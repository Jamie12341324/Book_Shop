import stripe
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from .forms import ProductForm
from .models import Product
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

stripe_public_key = settings.STRIPE_PUBLIC_KEY
stripe_secret_key = settings.STRIPE_SECRET_KEY

stripe.api_key = settings.STRIPE_SECRET_KEY

def product_list(request):
    template='products/product_list.html'
    products=Product.objects.values()
    context = {
        'products':products,
    }
    return render(request,template,context)

@login_required(login_url="/accounts/login/")
def product_details(request,product_id):
    if request.method=="GET":
        product=Product.objects.get(id=product_id)
        template='products/product_detail.html'
        context={
            'product':product,
        }
        return render(request,template,context)
    
def create_checkout_session(request, product_id):

    if request.method != 'POST':

        return redirect('product_list')
 
    product = get_object_or_404(Product, id=product_id)

    try:

        session = stripe.checkout.Session.create(    
            payment_method_types=['card'],
            customer_creation='always',
            billing_address_collection='required',
            shipping_address_collection={"allowed_countries": ["GB", "US"]},
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'unit_amount_decimal': product.price*100,       # from the database
                    'product_data': {
                        'name': product.title,         # from the database
                        'description': product.description,
                    },
                },
                'quantity': 1,
            }],

            mode='payment',

            # Store product_id in metadata so success view can look it up

            metadata={'product_id': product.id},

            success_url=(
                request.build_absolute_uri('/products/success/')
                + '?session_id={CHECKOUT_SESSION_ID}'
            ),

            cancel_url=request.build_absolute_uri('/products/cancel/'),
        )

        return redirect(session.url, code=303)
 
    except stripe.error.StripeError as e:

        return render(request, '/products/error.html', {'error': str(e)})
    
def payment_success(request):

    session_id = request.GET.get('session_id')

    order = None
 
    if session_id:
        #session = stripe.checkout.Session.retrieve(session_id)
        #shipping_address = shipping.address
        #print('shipping code' + shipping["postal_code"])
        try:

            session = stripe.checkout.Session.retrieve(session_id)
            #shipping = session.shipping_details
            #shipping_address = shipping.address
    
            # Guard: avoid duplicate rows if user refreshes the success page
            # print('address' + session.shipping_details.address)
            if not Order.objects.filter(stripe_session_id=session_id).exists():
                product_id =  session.metadata['product_id']
                product    = get_object_or_404(Product, id=product_id)
                order = Order.objects.create(
                    product           = product,
                    stripe_session_id = session_id,
                    customer_email    = session.customer_details.email,
                    amount_paid       = session.amount_total,
                    currency          = session.currency.upper(),
                    status            = 'complete',
             #       shipping_address_name = shipping["name"],
             #       shipping_address = shipping_address["address"]["line1"],
             #       shipping_address_postcode = shipping["postal_code"],
             #       shipping_address_country = shipping["country"],
                )

            else:

                order = Order.objects.get(stripe_session_id=session_id)
 
        except (stripe.error.StripeError, Exception):
            pass
 
    return render(request, 'products/success.html', {'order': order})

def payment_cancel(request):

    return render(request, 'products/cancel.html')

@csrf_exempt
def stripe_webhook(request):


    payload    = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    secret     = settings.STRIPE_WEBHOOK_SECRET
                
    if True:
        event = stripe.Webhook.construct_event(
            payload, sig_header, secret
        )
        session    = event['data']['object']
        session_id = session['id']
        product_id = session['metadata']['product_id']
        product = Product.objects.get(id=product_id)

        shipping = session.get("shipping_details")
        name = "?"
        if shipping:
            name = shipping.get("name")
            
        Order.objects.create(
                            product           = product,
                            stripe_session_id = session_id,
                            customer_email    = session['customer_details']['email'],
                            amount_paid       = session['amount_total'],
                            currency          = session['currency'].upper(),
                            status            = 'confirmed',
                            shipping_address_name = name,
                        )
    
    # ── Step 1: Verify the event came from Stripe ──────────────────

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, secret
        )

    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        # Invalid signature — request did not come from Stripe
        return HttpResponse(status=400)
 
    #return HttpResponse(status=200)

    # ── Step 2: Handle the event type ──────────────────────────────

    if event['type'] == 'checkout.session.completed':

        session    = event['data']['object']
        session_id = session['id']

        if not Order.objects.filter(stripe_session_id=session_id).exists():

            try:
                product_id = session['metadata']['product_id']

            except (KeyError, TypeError):
                    product_id = None

            if not product_id:
                    print_msg = ("ℹ️ No product_id in metadata — skipping order creation")
            else:
                    product = Product.objects.get(id=product_id)
                    Order.objects.create(...)
            if not product_id:

                print_msg = ("ℹ️ Webhook: no product_id in metadata (test trigger?), skipping.")


            else:

                try:

                    product = Product.objects.get(id=product_id)
                    #shipping = session.get("shipping_details")
                    #name = "?"
                    #if shipping:
                    #    name = shipping.get("name")

                    Order.objects.create(
                        product           = product,
                        stripe_session_id = session_id,
                        customer_email    = session['customer_details']['email'],
                        amount_paid       = session['amount_total'],
                        currency          = session['currency'].upper(),
                        status            = 'confirmed2',
                        
                    )

                    print_msg = (f"✅ Webhook: Order created for {product.name}")

                except Product.DoesNotExist:

                    print_msg = (f"❌ Webhook: Product {product_id} not found")
 
    elif event['type'] == 'payment_intent.payment_failed':

        session = event['data']['object']

        print_msg = (f"❌ Payment failed: {session.get('last_payment_error', {}).get('message')}")
 
    else:

        print_msg = (f"ℹ️  Unhandled event type: {event['type']}")
 
    # ── Step 3: Always return 200 so Stripe knows we received it ───

    return HttpResponse(status=200)

