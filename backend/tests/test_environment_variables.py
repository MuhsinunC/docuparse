import os

print("--- Testing Environment Variables ---")

print("Listing all environment variables found:")

if not os.environ:
    print("No environment variables found.")
else:
    # Iterate through environment variables without sorting
    for key, value in os.environ.items():
        # Be cautious about printing sensitive values in real logs
        # For this test, we'll print them to verify they are set.
        print(f"{key}={value}")

print("--- Finished Testing Environment Variables ---")

# Minimal pytest compatibility (optional, makes it runnable with pytest)
def test_env_vars_print():
    assert True # Just a placeholder to make pytest happy 