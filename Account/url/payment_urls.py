from django.urls import path

from ..views.payment import khalti_view as khalti_view
from ..views.payment import transaction_view as transaction_view
from ..views.payment import voucher_view as voucher_view

urlpatterns = [
  path('transaction', transaction_view.transaction),
  path('due/<str:username>', transaction_view.due),
  path('payment/details/<str:username>', transaction_view.StudentPaymentDetails),
  path('bulk', transaction_view.bulkBillAdd),
  path('khalti', khalti_view.khaltiVerify),
  path('voucher', voucher_view.addVoucher),
  path('unverified/voucher', voucher_view.unverifiedVoucher),
  path('verify/voucher', voucher_view.verifyVoucher),
  path('due/<str:username>/<int:semester>', transaction_view.semesterDue),
]