import stripe
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from .forms import ProductForm
from .models import Product
from .models import Order
from django.db.models import Q
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
        if False:
            customer = stripe.Customer.create(
                email="alice@example.com",
                shipping={
                    "name": "Colin Smith",
                    "address": {
                    "line1": "1 High Street",
                    "line2": "Cheapside",
                    "city": "Bath",
                    "postal_code": "BA1 1AA",
                    "country": "GB",
                    },
                },
            )
        

        session = stripe.checkout.Session.create(    
            payment_method_types=['card'],
            customer_creation='always',
            #customer = customer.id,
            billing_address_collection='required',
            shipping_address_collection={"allowed_countries": ["GB", "US"]},
            phone_number_collection={ 
                'enabled': True,  
            },
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

            metadata={'product_id': product.id,'user_id':request.user.id},

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
    #print('session1')
    session = stripe.checkout.Session.retrieve(session_id)
    #print(session)
    if session_id:
        
        try:

            session = stripe.checkout.Session.retrieve(session_id)
            product_id = session['metadata']['product_id']
            product = Product.objects.get(id=product_id)

            shipping_address = session.collected_information.shipping_details.address
            shipping_name    = session.collected_information.shipping_details.name
            
            # Deal with possible null line2 value
            shipping_address_line2 = shipping_address.line2
            #print(shipping_address_line2)
            if shipping_address_line2 == None:
                shipping_address_line2 = ""

            billing_address = session.customer_details.address
            billing_name    = session.customer_details.name
            email           = session.customer_details.email
            phone           = session.customer_details.phone
            # Deal with possible null line2 value
            billing_address_line2 = billing_address.line2
            #print(billing_address_line2)
            if billing_address_line2 == None:
                billing_address_line2 = ""

            # Guard: avoid duplicate rows if user refreshes the success page
            # print('address' + session.shipping_details.address)
            #print("session2")
            if not Order.objects.filter(stripe_session_id=session_id).exists():
                order = Order.objects.create(
                    user = request.user,
                    product           = product,
                    stripe_session_id = session_id,
                    customer_email    = session.customer_details.email,
                    amount_paid       = session.amount_total,
                    currency          = session.currency.upper(),
                    status            = 'complete',
                    email = email,
                    phone = phone,
                    shipping_address_name = shipping_name,
                    shipping_address_line1 = shipping_address.line1,
                    shipping_address_line2 = shipping_address_line2,
                    shipping_address_city = shipping_address.city,
                    shipping_address_country = shipping_address.country,
                    shipping_address_postcode = shipping_address.postal_code,
                    billing_address_name = billing_name,
                    billing_address_line1 = billing_address.line1,
                    billing_address_line2 = billing_address_line2,
                    billing_address_city = billing_address.city,
                    billing_address_country = billing_address.country,
                    billing_address_postcode = billing_address.postal_code,
                )
                print('success complete')
            else:
                #print(session.amount_total)
                #product_to_change=Product.objects.get(Q(id=product_id))
                order = Order.objects.get(Q(stripe_session_id=session_id))
                #order.product = product
                #order.stripe_session_id = session_id,
                #order.customer_email    = session.customer_details.email,
                #order.amount_paid       = session.amount_total,
                #order.currency          = session.currency.upper(),
                #order.status            = 'complete2',
                #order.shipping_address_name = 'name',               
                #order.save()
                #print("print session3")
 
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
                
    if False:
        event = stripe.Webhook.construct_event(
            payload, sig_header, secret
        )
        session    = event['data']['object']
        session_id = session['id']
        product_id = session['metadata']['product_id']
        product = Product.objects.get(id=product_id)

        # Deal with possible null line2 which is optional
        
        shipping_line2 = session['collected_information']['shipping_details']['address']['line2']
        if shipping_line2 == None:
            shipping_line2 = ""

        billing_line2 = session['customer_details']['address']['line2']
        if billing_line2 == None:
            billing_line2 = ""

        Order.objects.create(
                            user = request.user,
                            product           = product,
                            stripe_session_id = session_id,
                            customer_email    = session['customer_details']['email'],
                            amount_paid       = session['amount_total'],
                            currency          = session['currency'].upper(),
                            status            = 'confirmed',
                            email                     = session['customer_details']['email'],
                            phone                     = session['customer_details']['phone'],
                            billing_address_name      = session['customer_details']['name'],
                            billing_address_line1     = session['customer_details']['address']['line1'],
                            billing_address_line2     = billing_line2,
                            billing_address_city      = session['customer_details']['address']['city'],
                            billing_address_postcode  = session['customer_details']['address']['postal_code'],
                            billing_address_country   = session['customer_details']['address']['country'],

                            shipping_address_name     = session['collected_information']['shipping_details']['name'],
                            shipping_address_line1    = session['collected_information']['shipping_details']['address']['line1'],
                            shipping_address_line2    = shipping_line2,
                            shipping_address_city     = session['collected_information']['shipping_details']['address']['city'],
                            shipping_address_postcode = session['collected_information']['shipping_details']['address']['postal_code'],
                            shipping_address_country  = session['collected_information']['shipping_details']['address']['country'], 
                        )

        return HttpResponse(status=200)


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
                    #Order.objects.create(...)
            if not product_id:

                print_msg = ("ℹ️ Webhook: no product_id in metadata (test trigger?), skipping.")


            else:

                try:

                    
                    session    = event['data']['object']
                    session_id = session['id']
                    product_id = session['metadata']['product_id']
                    product = Product.objects.get(id=product_id)
                    user_id = session['metadata']['user_id']
                    

                    # Deal with possible null line2 which is optional
        
                    shipping_line2 = session['collected_information']['shipping_details']['address']['line2']
                    if shipping_line2 == None:
                        shipping_line2 = ""

                    billing_line2 = session['customer_details']['address']['line2']
                    if billing_line2 == None:
                        billing_line2 = ""

                    Order.objects.create(
                            user = user_id,
                            product           = product,
                            stripe_session_id = session_id,
                            customer_email    = session['customer_details']['email'],
                            amount_paid       = session['amount_total'],
                            currency          = session['currency'].upper(),
                            status            = 'confirmed',
                            email                     = session['customer_details']['email'],
                            phone                     = session['customer_details']['phone'],
                            billing_address_name      = session['customer_details']['name'],
                            billing_address_line1     = session['customer_details']['address']['line1'],
                            billing_address_line2     = billing_line2,
                            billing_address_city      = session['customer_details']['address']['city'],
                            billing_address_postcode  = session['customer_details']['address']['postal_code'],
                            billing_address_country   = session['customer_details']['address']['country'],

                            shipping_address_name     = session['collected_information']['shipping_details']['name'],
                            shipping_address_line1    = session['collected_information']['shipping_details']['address']['line1'],
                            shipping_address_line2    = shipping_line2,
                            shipping_address_city     = session['collected_information']['shipping_details']['address']['city'],
                            shipping_address_postcode = session['collected_information']['shipping_details']['address']['postal_code'],
                            shipping_address_country  = session['collected_information']['shipping_details']['address']['country'],
                        )

                    #Order.objects.create(
                    #    product           = product,
                    #    stripe_session_id = session_id,
                    #    customer_email    = session['customer_details']['email'],
                    #    amount_paid       = session['amount_total'],
                    #    currency          = session['currency'].upper(),
                    #    status            = 'confirmed',   
                    #)

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

