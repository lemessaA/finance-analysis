"""
M-Pesa Payment Schemas

Pydantic models for M-Pesa payment requests and responses.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class STKPushRequest(BaseModel):
    """STK Push payment request model."""
    phone_number: str = Field(..., description="Customer phone number (254XXXXXXXXX)")
    amount: int = Field(..., ge=1, le=150000, description="Amount to pay (1-150,000 KES)")
    account_reference: str = Field(..., max_length=12, description="Account reference")
    transaction_desc: str = Field(..., max_length=13, description="Transaction description")
    callback_url: Optional[str] = Field(None, description="Callback URL for this transaction")


class STKPushResponse(BaseModel):
    """STK Push response model."""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Response message")
    checkout_request_id: Optional[str] = Field(None, description="Checkout request ID")
    merchant_request_id: Optional[str] = Field(None, description="Merchant request ID")
    response_code: Optional[str] = Field(None, description="M-Pesa response code")
    response_description: Optional[str] = Field(None, description="Response description")
    customer_message: Optional[str] = Field(None, description="Message to show customer")


class B2CPaymentRequest(BaseModel):
    """B2C payment request model."""
    phone_number: str = Field(..., description="Recipient phone number")
    amount: int = Field(..., ge=1, le=150000, description="Amount to send (1-150,000 KES)")
    remarks: str = Field("", max_length=100, description="Payment remarks")
    command_id: str = Field("SalaryPayment", description="Command ID")
    occasion: str = Field("", max_length=100, description="Payment occasion")


class TransactionStatusRequest(BaseModel):
    """Transaction status query request."""
    checkout_request_id: str = Field(..., description="Checkout request ID to query")


class CallbackData(BaseModel):
    """M-Pesa callback data model."""
    TransactionType: str
    TransID: str
    TransTime: str
    TransAmount: str
    BusinessShortCode: str
    BillRefNumber: str
    InvoiceNumber: str
    OrgAccountBalance: str
    ThirdPartyTransID: str
    PhoneNumber: str
    FirstName: str
    MiddleName: str
    LastName: str


class PaymentConfirmation(BaseModel):
    """Payment confirmation model."""
    transaction_id: str = Field(..., description="M-Pesa transaction ID")
    phone_number: str = Field(..., description="Customer phone number")
    amount: float = Field(..., description="Transaction amount")
    account_reference: str = Field(..., description="Account reference")
    transaction_date: str = Field(..., description="Transaction date")
    status: str = Field(..., description="Transaction status")


class PaymentHistory(BaseModel):
    """Payment history response model."""
    payments: List[PaymentConfirmation] = Field(default_factory=list)
    total_count: int = Field(default=0)
    page: int = Field(default=1)
    per_page: int = Field(default=10)


class MpesaConfigRequest(BaseModel):
    """M-Pesa configuration request."""
    consumer_key: str = Field(..., description="M-Pesa consumer key")
    consumer_secret: str = Field(..., description="M-Pesa consumer secret")
    passkey: str = Field(..., description="M-Pesa passkey")
    shortcode: str = Field(..., description="Business shortcode")
    initiator_name: str = Field(..., description="B2C initiator name")
    environment: str = Field("sandbox", description="Environment (sandbox/production)")
    callback_url: str = Field(..., description="Callback URL")
    confirmation_url: Optional[str] = Field(None, description="Confirmation URL")
    validation_url: Optional[str] = Field(None, description="Validation URL")
