from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/pay', methods=['GET'])
def pay():
    return render_template('pay_order.html')


@app.route('/purchase', methods=['POST'])
def purchase():
    pay_status = {"success": False, "pay_id": None}
    if request.form['hidden'] == 'SuperSecretPayElement' and 'razorpay_payment_id' in request.form:
        pay_status['success'] = True
        pay_status['pay_id'] = request.form['razorpay_payment_id']
    return render_template('purchase.html', success=pay_status['success'], pay_id=pay_status['pay_id'])


if __name__ == '__main__':
    app.debug = True
    app.run()
