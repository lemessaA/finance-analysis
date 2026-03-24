# M-Pesa Payment Integration

This document outlines the M-Pesa payment integration for Business Insights platform.

## Overview

The M-Pesa integration enables businesses to:
- Accept payments from customers via STK Push in Ethiopia
- Send money to customers (B2C)
- Query transaction status
- View payment history
- Manage account balance

## Features Implemented

### 📱 Payment Methods
- **STK Push**: Send payment requests to customer phones
- **B2C Payment**: Disburse payments to customers
- **Transaction Status**: Check payment completion status
- **Payment History**: View all transaction records
- **Account Balance**: Monitor available funds

### 🔐 Security Features
- OAuth 2.0 authentication with M-Pesa API
- Encrypted transaction requests
- Callback URL validation
- Phone number format validation (Ethiopian format: 251XXXXXXXXX)
- Amount limits (1-150,000 ETB)

### 🌐 API Endpoints

#### Frontend Routes
- `/mpesa` - Main payment interface
- `/api/v1/mpesa/*` - Backend API endpoints

#### Backend API Routes
```
POST /api/v1/mpesa/stk-push          - Initiate STK Push payment
POST /api/v1/mpesa/transaction-status  - Query transaction status
POST /api/v1/mpesa/b2c-payment       - Process B2C payment
POST /api/v1/mpesa/callback           - Receive M-Pesa callbacks
GET  /api/v1/mpesa/payment-history     - Get payment history
GET  /api/v1/mpesa/transaction/{id}    - Get transaction details
GET  /api/v1/mpesa/balance            - Get account balance
```

## Configuration

### Environment Variables
```bash
# M-Pesa API Configuration
MPESA_CONSUMER_KEY="your_consumer_key"
MPESA_CONSUMER_SECRET="your_consumer_secret"
MPESA_PASSKEY="your_passkey"
MPESA_SHORTCODE="your_business_shortcode"
MPESA_INITIATOR_NAME="your_initiator_name"
MPESA_ENVIRONMENT="sandbox"  # or "production"
MPESA_CALLBACK_URL="https://yourdomain.com/api/v1/mpesa/callback"
MPESA_CONFIRMATION_URL="https://yourdomain.com/api/v1/mpesa/confirmation"
MPESA_VALIDATION_URL="https://yourdomain.com/api/v1/mpesa/validation"
```

### Setup Instructions

1. **Get M-Pesa API Credentials**
   - Visit [Safaricom Ethiopia Developer Portal](https://developer.safaricom.et/)
   - Create an account and register your application
   - Get Consumer Key, Consumer Secret, and Passkey
   - Configure your Business Shortcode

2. **Configure Environment**
   - Add credentials to your `.env` file
   - Set environment to `sandbox` for testing
   - Configure callback URLs for production

3. **Test Integration**
   - Use sandbox environment for initial testing
   - Verify STK Push functionality
   - Test callback handling

4. **Go Live**
   - Switch to production environment
   - Update callback URLs to production endpoints
   - Monitor transactions through dashboard

## Usage Examples

### STK Push Payment
```javascript
const paymentRequest = {
  phone_number: "251712345678",
  amount: 1000,
  account_reference: "INV-001",
  transaction_desc: "Payment for goods"
};

const response = await apiClient.post('/api/v1/mpesa/stk-push', paymentRequest);
```

### Check Transaction Status
```javascript
const statusRequest = {
  checkout_request_id: "ws_CO_123456789"
};

const response = await apiClient.post('/api/v1/mpesa/transaction-status', statusRequest);
```

## Error Handling

### Common Response Codes
- `0` - Success
- `1` - Insufficient funds
- `1032` - Request cancelled by user
- `1037` - Duplicate transaction
- `2001` - Invalid phone number format
- `2002` - Invalid amount

### Error Response Format
```json
{
  "success": false,
  "message": "Payment failed: Invalid phone number format",
  "response_code": "2001",
  "response_description": "Invalid phone number format"
}
```

## Security Considerations

### 🔒 Best Practices
1. **Never expose credentials** in frontend code
2. **Use HTTPS** for all callback URLs
3. **Validate all inputs** before processing
4. **Implement rate limiting** to prevent abuse
5. **Log all transactions** for audit purposes
6. **Monitor callbacks** for payment confirmations

### 🛡️ Protection Measures
- Phone number format validation
- Amount range validation (1-150,000 ETB)
- Request timeout handling
- Duplicate transaction prevention
- Secure callback processing

## Testing

### Sandbox Environment
- Use test credentials provided by Safaricom Ethiopia
- Test with small amounts
- Verify callback functionality
- Monitor transaction status updates

### Production Deployment
- Use production credentials
- Implement proper error handling
- Set up monitoring and alerts
- Test end-to-end payment flow

## Support

For M-Pesa API support:
- Developer Portal: https://developer.safaricom.et/
- Documentation: Available in developer portal
- Technical Support: Contact Safaricom Ethiopia business support

## Troubleshooting

### Common Issues
1. **Authentication failures** - Check consumer key/secret
2. **Invalid phone numbers** - Ensure 251XXXXXXXXX format
3. **Callback timeouts** - Verify URL accessibility
4. **Amount rejections** - Check account balance and limits

### Debug Tips
- Check backend logs for detailed error messages
- Verify API credentials are correctly set
- Test with known good phone numbers
- Monitor network connectivity to M-Pesa APIs
