"""
M-Pesa Payment API Routes

API endpoints for M-Pesa payment processing including STK Push, B2C, 
transaction status queries, and payment history with enhanced error handling.
"""

from __future__ import annotations

import uuid
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from app.schemas.mpesa import (
    STKPushRequest, STKPushResponse, B2CPaymentRequest,
    TransactionStatusRequest, PaymentHistory, CallbackData
)
from app.services.mpesa_service import get_mpesa_service
from app.exceptions.mpesa_exceptions import (
    MpesaException, MpesaValidationError, MpesaTransactionError,
    MpesaConfigurationError, MpesaErrorCode
)
from app.validators.mpesa_validator import (
    MpesaInputValidator, ValidatedSTKPushRequest,
    ValidatedTransactionStatusRequest, ValidatedB2CPaymentRequest
)
from app.logging.mpesa_logger import get_mpesa_logger

# Initialize M-Pesa logger
logger = get_mpesa_logger()
router = APIRouter()

# In-memory store for demo (replace with database in production)
TRANSACTION_STORE: Dict[str, Dict[str, Any]] = {}


@router.post(
    "/stk-push",
    response_model=STKPushResponse,
    status_code=status.HTTP_200_OK,
    summary="Initiate STK Push Payment",
    description="Send money request to customer's M-Pesa account"
)
async def stk_push_payment(request: STKPushRequest):
    """Initiate STK Push payment with enhanced validation and error handling."""
    try:
        # Validate request using Pydantic model
        validated_request = ValidatedSTKPushRequest(**request.dict())
        
        logger.info(
            "STK Push payment request received",
            phone_number=validated_request.phone_number,
            amount=validated_request.amount,
            account_reference=validated_request.account_reference
        )
        
        mpesa = await get_mpesa_service()
        
        # Create STK push request
        stk_request = STKPushRequest(
            phone_number=validated_request.phone_number,
            amount=validated_request.amount,
            account_reference=validated_request.account_reference,
            transaction_desc=validated_request.transaction_desc,
            callback_url=request.callback_url
        )
        
        # Process payment
        response = await mpesa.stk_push(stk_request)
        
        # Store transaction for tracking
        if response.checkout_request_id:
            TRANSACTION_STORE[response.checkout_request_id] = {
                "phone_number": validated_request.phone_number,
                "amount": validated_request.amount,
                "account_reference": validated_request.account_reference,
                "transaction_desc": validated_request.transaction_desc,
                "status": "pending" if response.success else "failed",
                "created_at": str(uuid.uuid4()),
                "checkout_request_id": response.checkout_request_id,
                "merchant_request_id": response.merchant_request_id
            }
            
            logger.info(
                "STK Push transaction stored",
                checkout_request_id=response.checkout_request_id,
                success=response.success
            )
        
        return response
        
    except MpesaValidationError as e:
        logger.warning(
            "STK Push validation failed",
            exception=e,
            details=e.details
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": e.to_dict(),
                "message": "Validation failed"
            }
        )
        
    except MpesaConfigurationError as e:
        logger.error(
            "STK Push configuration error",
            exception=e,
            details=e.details
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": e.to_dict(),
                "message": "Service configuration error"
            }
        )
        
    except MpesaTransactionError as e:
        logger.error(
            "STK Push transaction error",
            exception=e,
            details=e.details
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": e.to_dict(),
                "message": "Transaction processing error"
            }
        )
        
    except MpesaException as e:
        logger.error(
            "STK Push M-Pesa error",
            exception=e,
            details=e.details
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": e.to_dict(),
                "message": "Payment processing error"
            }
        )
        
    except Exception as e:
        logger.error(
            "STK Push unexpected error",
            exception=e
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": MpesaErrorCode.UNKNOWN_ERROR.value,
                "message": "Unexpected error occurred",
                "details": {"error": str(e)}
            }
        )


@router.post(
    "/transaction-status",
    response_model=STKPushResponse,
    status_code=status.HTTP_200_OK,
    summary="Query Transaction Status",
    description="Check the status of an M-Pesa transaction"
)
async def query_transaction_status(request: TransactionStatusRequest):
    """Query STK Push transaction status."""
    try:
        mpesa = await get_mpesa_service()
        response = await mpesa.query_transaction_status(request.checkout_request_id)
        
        # Update stored transaction status
        if request.checkout_request_id in TRANSACTION_STORE:
            TRANSACTION_STORE[request.checkout_request_id]["status"] = "completed" if response.success else "failed"
            TRANSACTION_STORE[request.checkout_request_id]["response_code"] = response.response_code
            TRANSACTION_STORE[request.checkout_request_id]["response_description"] = response.response_description
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transaction status query error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Status query failed: {str(e)}"
        )


@router.post(
    "/b2c-payment",
    response_model=STKPushResponse,
    status_code=status.HTTP_200_OK,
    summary="B2C Payment",
    description="Send money from business account to customer M-Pesa"
)
async def b2c_payment(request: B2CPaymentRequest):
    """Process B2C payment."""
    try:
        # Validate phone number
        if not request.phone_number.startswith("251") or len(request.phone_number) != 12:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number format. Use 251XXXXXXXXX format"
            )
        
        # Validate amount
        if request.amount < 1 or request.amount > 150000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount must be between 1 and 150,000 ETB"
            )
        
        mpesa = await get_mpesa_service()
        response = await mpesa.b2c_payment(
            phone_number=request.phone_number,
            amount=request.amount,
            remarks=request.remarks
        )
        
        # Store B2C transaction
        transaction_id = str(uuid.uuid4())
        TRANSACTION_STORE[transaction_id] = {
            "phone_number": request.phone_number,
            "amount": request.amount,
            "remarks": request.remarks,
            "transaction_type": "b2c",
            "status": "completed" if response.success else "failed",
            "created_at": transaction_id,
            "response_code": response.response_code
        }
        
        logger.info(f"B2C payment processed: {transaction_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"B2C payment error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"B2C payment failed: {str(e)}"
        )


@router.post(
    "/callback",
    status_code=status.HTTP_200_OK,
    summary="M-Pesa Callback",
    description="Receive payment confirmation callbacks from M-Pesa"
)
async def mpesa_callback(callback_data: Dict[str, Any]):
    """Handle M-Pesa payment callbacks."""
    try:
        # Log callback for debugging
        logger.info(f"M-Pesa callback received: {callback_data}")
        
        # Process callback based on transaction type
        if "Body" in callback_data and "stkCallback" in callback_data["Body"]:
            # STK Push callback
            callback_result = callback_data["Body"]["stkCallback"]
            
            if callback_result.get("ResultCode") == "0":
                # Successful payment
                merchant_request_id = callback_result.get("MerchantRequestID")
                checkout_request_id = callback_result.get("CheckoutRequestID")
                
                # Update transaction status
                if checkout_request_id in TRANSACTION_STORE:
                    TRANSACTION_STORE[checkout_request_id].update({
                        "status": "completed",
                        "mpesa_transaction_id": callback_result.get("Result", {}).get("TransID"),
                        "amount": callback_result.get("Result", {}).get("Amount"),
                        "phone_number": callback_result.get("Result", {}).get("PhoneNumber"),
                        "completed_at": callback_result.get("Result", {}).get("TransTime")
                    })
                
                logger.info(f"Payment successful: {checkout_request_id}")
            else:
                # Failed payment
                checkout_request_id = callback_result.get("CheckoutRequestID")
                if checkout_request_id in TRANSACTION_STORE:
                    TRANSACTION_STORE[checkout_request_id].update({
                        "status": "failed",
                        "error_code": callback_result.get("ResultCode"),
                        "error_description": callback_result.get("ResultDesc")
                    })
                
                logger.error(f"Payment failed: {checkout_request_id}")
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Callback processing error: {e}")
        return {"status": "error", "message": str(e)}


@router.get(
    "/payment-history",
    response_model=PaymentHistory,
    status_code=status.HTTP_200_OK,
    summary="Payment History",
    description="Get history of M-Pesa transactions"
)
async def get_payment_history(page: int = 1, per_page: int = 10):
    """Get payment history."""
    try:
        # Get all transactions (in production, this would query database)
        all_transactions = list(TRANSACTION_STORE.values())
        
        # Sort by creation date (newest first)
        all_transactions.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # Paginate
        start = (page - 1) * per_page
        end = start + per_page
        paginated_transactions = all_transactions[start:end]
        
        return PaymentHistory(
            payments=paginated_transactions,
            total_count=len(all_transactions),
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        logger.error(f"Payment history error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get payment history: {str(e)}"
        )


@router.get(
    "/transaction/{transaction_id}",
    status_code=status.HTTP_200_OK,
    summary="Get Transaction Details",
    description="Get details of a specific transaction"
)
async def get_transaction_details(transaction_id: str):
    """Get transaction details by ID."""
    try:
        if transaction_id not in TRANSACTION_STORE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        return TRANSACTION_STORE[transaction_id]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transaction details error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get transaction details: {str(e)}"
        )


@router.get(
    "/balance",
    status_code=status.HTTP_200_OK,
    summary="Get Account Balance",
    description="Get M-Pesa account balance"
)
async def get_account_balance():
    """Get account balance (placeholder implementation)."""
    try:
        # This would require B2B balance query API in production
        # For now, return mock data
        return {
            "account_balance": 50000.00,
            "available_balance": 45000.00,
            "currency": "ETB",
            "last_updated": "2024-03-24T12:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Balance query error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get balance: {str(e)}"
        )
