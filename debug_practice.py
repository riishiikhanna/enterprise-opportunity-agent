
from validators import is_supported_fact

customer_requirement = (
    "We do not have $5 million available."
)

fact = "Have $5 million available"

print("Starting evidence validation...")

result = is_supported_fact(
    fact,
    customer_requirement
)

print("Validation result:", result)