# M-Pesa Enhanced Error Handling & Logging Implementation

## Overview

This document outlines the comprehensive enhancements made to the M-Pesa payment system, including centralized error handling, advanced logging, input validation, retry logic, and graceful failure handling.

## 🏗️ Architecture Enhancements

### 1. Custom Exception System (`app/exceptions/mpesa_exceptions.py`)

#### **Exception Hierarchy:**
```
MpesaException (Base)
├── MpesaAuthenticationError
├── MpesaValidationError  
├── MpesaAPIError
├── MpesaTransactionError
├── MpesaConfigurationError
└── MpesaRetryableError
```

#### **Error Codes:**
- **AUTH_001-003**: Authentication failures
- **VAL_001-004**: Input validation errors
- **API_001-004**: API communication errors
- **TXN_001-005**: Transaction processing errors
- **SYS_001-999**: System configuration errors

#### **Features:**
- Structured error details
- Error categorization
- Original exception preservation
- JSON serialization support

### 2. Input Validation System (`app/validators/mpesa_validator.py`)

#### **Validation Rules:**
```python
# Phone Number: Ethiopian format (251XXXXXXXXX)
ETHIOPIAN_PHONE_REGEX = r'^251[0-9]{9}$'

# Amount: 1-150,000 ETB
MIN_AMOUNT = 1
MAX_AMOUNT = 150000

# Account Reference: Max 12 chars, alphanumeric
ACCOUNT_REF_MAX_LENGTH = 12

# Transaction Description: Max 13 chars
TRANSACTION_DESC_MAX_LENGTH = 13
```

#### **Validators:**
- **Phone Number**: Ethiopian format normalization
- **Amount**: Range and type validation
- **Account Reference**: Character and length validation
- **Transaction Description**: Length validation
- **Pydantic Models**: Automated validation

#### **Features:**
- Detailed error messages
- Field-specific validation
- Input normalization
- Pydantic integration

### 3. Advanced Logging System (`app/logging/mpesa_logger.py`)

#### **Log Categories:**
- **AUTHENTICATION**: Login/token events
- **VALIDATION**: Input validation results
- **API_CALL**: External API interactions
- **TRANSACTION**: Payment processing
- **CALLBACK**: Webhook processing
- **ERROR**: Error events
- **SYSTEM**: System events
- **SECURITY**: Security events

#### **Log Features:**
```python
# Structured JSON logging
{
  "timestamp": "2024-03-24T17:30:00.000Z",
  "service": "mpesa",
  "level": "INFO",
  "category": "TRANSACTION",
  "message": "STK Push initiated successfully",
  "transaction_id": "ws_CO_123456789",
  "phone_number": "251712XXX78",
  "amount": 1000,
  "success": true
}
```

#### **Output Destinations:**
- **Console**: Real-time monitoring
- **File**: Persistent logging (`logs/mpesa.log`)
- **JSON Format**: Structured parsing
- **Text Format**: Human readable

### 4. Retry Logic System (`app/retry/mpesa_retry.py`)

#### **Retry Strategies:**
- **Exponential Backoff**: Default for API calls
- **Fixed Delay**: Consistent retry intervals
- **Linear Backoff**: Gradual increase
- **No Retry**: For non-retryable errors

#### **Circuit Breaker:**
```python
# Prevents cascade failures
failure_threshold = 5
recovery_timeout = 60.0
states = ["CLOSED", "OPEN", "HALF_OPEN"]
```

#### **Retry Configuration:**
```python
RetryConfig(
    max_retries=3,
    base_delay=1.0,
    max_delay=30.0,
    backoff_multiplier=2.0,
    jitter=True
)
```

#### **Features:**
- Configurable retry policies
- Jitter for thundering herd prevention
- Circuit breaker pattern
- Detailed retry metrics

## 🔧 Implementation Details

### Enhanced M-Pesa Service (`app/services/mpesa_service.py`)

#### **Configuration Validation:**
```python
def _validate_config(self):
    missing_fields = []
    if not self.config.consumer_key:
        missing_fields.append("consumer_key")
    # ... validation for all required fields
    
    if missing_fields:
        raise MpesaConfigurationError(error_msg, missing_fields)
```

#### **Enhanced Authentication:**
```python
async def get_access_token(self) -> str:
    # Token caching with expiry check
    # Structured API call logging
    # Retry logic for transient failures
    # Detailed error reporting
```

#### **STK Push with Validation:**
```python
async def stk_push(self, request: STKPushRequest) -> PaymentResponse:
    # 1. Input validation
    validated_data = MpesaInputValidator.validate_stk_push_request(...)
    
    # 2. Transaction logging
    logger.log_transaction(...)
    
    # 3. API execution with retry
    result = await execute_mpesa_with_retry(...)
    
    # 4. Comprehensive error handling
    try:
        # ... API call logic
    except MpesaException as e:
        # ... structured error response
```

### Enhanced API Routes (`app/api/routes/mpesa.py`)

#### **Error Handling Pattern:**
```python
async def stk_push_payment(request: STKPushRequest):
    try:
        # Pydantic validation
        validated_request = ValidatedSTKPushRequest(**request.dict())
        
        # Business logic
        response = await mpesa.stk_push(stk_request)
        
        return response
        
    except MpesaValidationError as e:
        # 400 Bad Request with structured error
        raise HTTPException(status_code=400, detail={"error": e.to_dict()})
        
    except MpesaConfigurationError as e:
        # 500 Internal Server Error
        raise HTTPException(status_code=500, detail={"error": e.to_dict()})
        
    except MpesaException as e:
        # Generic M-Pesa error handling
        raise HTTPException(status_code=500, detail={"error": e.to_dict()})
        
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail={
            "error_code": MpesaErrorCode.UNKNOWN_ERROR.value,
            "message": "Unexpected error occurred"
        })
```

## 📊 Logging Examples

### Transaction Success:
```json
{
  "timestamp": "2024-03-24T17:30:15.123Z",
  "service": "mpesa",
  "level": "INFO",
  "category": "TRANSACTION",
  "message": "STK Push completed successfully",
  "transaction_id": "ws_CO_123456789",
  "checkout_request_id": "ws_CO_123456789",
  "phone_number": "251712XXX78",
  "amount": 1000,
  "success": true
}
```

### Validation Error:
```json
{
  "timestamp": "2024-03-24T17:30:20.456Z",
  "service": "mpesa",
  "level": "WARNING",
  "category": "VALIDATION",
  "message": "Validation Failed for phone_number",
  "field_name": "phone_number",
  "field_value": "254712345678",
  "success": false,
  "error_message": "Invalid Ethiopian phone number format. Use 251XXXXXXXXX"
}
```

### API Call with Retry:
```json
{
  "timestamp": "2024-03-24T17:30:25.789Z",
  "service": "mpesa",
  "level": "INFO",
  "category": "API",
  "message": "API Call: POST https://api.safaricom.et/mpesa/stkpush/v1/processrequest",
  "method": "POST",
  "url": "https://api.safaricom.et/mpesa/stkpush/v1/processrequest",
  "status_code": 200,
  "response_time_ms": 1250,
  "success": true,
  "retry_count": 2,
  "retry_delays": [1.0, 2.1]
}
```

## 🔄 Retry Logic Examples

### Exponential Backoff:
```
Attempt 1: Immediate
Attempt 2: Wait 1.0s (base_delay)
Attempt 3: Wait 2.0s (base_delay * 2^1)
Attempt 4: Wait 4.0s (base_delay * 2^2)
```

### With Jitter:
```
Attempt 2: Wait 0.95s (1.0s ± 10% jitter)
Attempt 3: Wait 2.3s (2.0s ± 10% jitter)
Attempt 4: Wait 4.2s (4.0s ± 10% jitter)
```

### Circuit Breaker:
```
State: CLOSED → OPEN (after 5 failures)
State: OPEN → HALF_OPEN (after 60s timeout)
State: HALF_OPEN → CLOSED (on success)
State: HALF_OPEN → OPEN (on failure)
```

## 🛡️ Security Features

### Phone Number Masking:
```python
# Original: 251712345678
# Masked: 251712XXX78
masked_phone = phone_number[:6] + "XXX" + phone_number[-2:]
```

### Sensitive Data Logging:
- No passwords in logs
- Masked phone numbers
- Token expiration times only
- Error details sanitized

### Security Events:
```python
logger.log_security_event(
    event_type="invalid_phone_format",
    severity="medium",
    details={"provided_format": "254712345678", "expected": "251XXXXXXXXX"}
)
```

## 📈 Performance Monitoring

### Metrics Tracked:
- **API Response Times**: All external calls
- **Retry Rates**: Failed vs successful retries
- **Error Rates**: By category and type
- **Transaction Success Rates**: By payment type
- **Circuit Breaker State**: Current status and transitions

### Health Checks:
```python
# Service health monitoring
- Configuration validation
- API connectivity tests
- Token refresh status
- Circuit breaker state
```

## 🚀 Usage Examples

### Basic Payment with Error Handling:
```python
try:
    response = await mpesa.stk_push(payment_request)
    if response.success:
        print("Payment initiated successfully")
    else:
        print(f"Payment failed: {response.message}")
        
except MpesaValidationError as e:
    print(f"Invalid input: {e.message}")
except MpesaTransactionError as e:
    print(f"Transaction failed: {e.message}")
except MpesaException as e:
    print(f"M-Pesa error: {e.message}")
```

### Custom Retry Configuration:
```python
custom_retry_config = RetryConfig(
    max_retries=5,
    base_delay=0.5,
    max_delay=60.0,
    strategy=RetryStrategy.LINEAR_BACKOFF,
    jitter=True
)

result = await execute_mpesa_with_retry(
    api_function,
    retry_config=custom_retry_config
)
```

### Logging Custom Events:
```python
logger.log_transaction(
    transaction_type="CUSTOM_PAYMENT",
    transaction_id="txn_123",
    phone_number="251712345678",
    amount=5000,
    status="processing",
    custom_field="custom_value"
)
```

## 🔍 Troubleshooting

### Common Issues:

1. **Configuration Errors**:
   - Check environment variables
   - Validate all required fields
   - Look for `MpesaConfigurationError`

2. **Validation Failures**:
   - Phone number format (251XXXXXXXXX)
   - Amount range (1-150,000 ETB)
   - Field length limits

3. **API Timeouts**:
   - Check retry configuration
   - Monitor circuit breaker state
   - Verify network connectivity

4. **Authentication Issues**:
   - Invalid credentials
   - Token expiry
   - Rate limiting

### Debug Information:
- Structured logs in `logs/mpesa.log`
- API call details with timing
- Retry attempts and delays
- Error codes and messages

## 📋 Configuration Checklist

### Environment Variables:
```bash
# Required
MPESA_CONSUMER_KEY="your_key"
MPESA_CONSUMER_SECRET="your_secret"
MPESA_PASSKEY="your_passkey"
MPESA_SHORTCODE="your_shortcode"
MPESA_INITIATOR_NAME="your_initiator"
MPESA_CALLBACK_URL="https://yourdomain.com/callback"

# Optional
MPESA_ENVIRONMENT="sandbox"
MPESA_CONFIRMATION_URL="https://yourdomain.com/confirmation"
MPESA_VALIDATION_URL="https://yourdomain.com/validation"
```

### Logging Configuration:
```python
# File logging
log_file = "logs/mpesa.log"

# Console output
console_output = True

# JSON format
json_format = True
```

### Retry Configuration:
```python
# Default settings
max_retries = 3
base_delay = 1.0
max_delay = 30.0
strategy = RetryStrategy.EXPONENTIAL_BACKOFF
jitter = True
```

## 🎯 Benefits Achieved

### ✅ **Centralized Error Handling**
- Consistent error responses
- Structured error information
- Proper HTTP status codes
- Error categorization

### ✅ **Advanced Logging**
- Structured JSON logs
- Multiple output destinations
- Transaction tracking
- Security event logging

### ✅ **Input Validation**
- Ethiopian phone format validation
- Amount range validation
- Field length checks
- Detailed error messages

### ✅ **Retry Logic**
- Configurable retry strategies
- Circuit breaker protection
- Jitter for load distribution
- Detailed retry metrics

### ✅ **Graceful Failure Handling**
- Never crashes the service
- Meaningful error messages
- Proper HTTP responses
- Fallback behaviors

### ✅ **Production Ready**
- Comprehensive monitoring
- Security best practices
- Performance tracking
- Troubleshooting support

The M-Pesa payment system is now enterprise-grade with robust error handling, comprehensive logging, and production-ready reliability features.
