from django.http import JsonResponse
from django.views.decorators.http import require_GET
from decimal import Decimal, InvalidOperation
from django.core.validators import ValidationError
from .models import ConversionRate

@require_GET
def convert_currency(request, currency1, currency2, amount_of_currency1):
    try:
        # Validate input parameters
        if not all([currency1, currency2, amount_of_currency1]):
            return JsonResponse(
                {'error': 'All parameters are required'},
                status=400
            )

        try:
            amount = Decimal(amount_of_currency1)
            if amount <= 0:
                raise ValidationError("Amount must be positive")
        except (InvalidOperation, ValidationError):
            return JsonResponse(
                {'error': 'Invalid amount value'},
                status=400
            )

        # Same currency conversion
        if currency1 == currency2:
            return JsonResponse({
                'converted_amount': str(amount.quantize(Decimal('0.01'))),
                'rate': '1.0',
                'from_currency': currency1,
                'to_currency': currency2
            })

        try:
            rate_obj = ConversionRate.objects.get(
                from_currency=currency1.upper(),
                to_currency=currency2.upper()
            )
            converted_amount = amount * rate_obj.rate

            return JsonResponse({
                'converted_amount': str(converted_amount.quantize(Decimal('0.01'))),
                'rate': str(rate_obj.rate),
                'from_currency': currency1,
                'to_currency': currency2,
                'last_updated': rate_obj.last_updated.isoformat()
            })

        except ConversionRate.DoesNotExist:
            return JsonResponse(
                {'error': f'Conversion rate from {currency1} to {currency2} not available'},
                status=404
            )

    except Exception as e:
        return JsonResponse(
            {'error': f'Server error: {str(e)}'},
            status=500
        )