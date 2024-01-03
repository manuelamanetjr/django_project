#include <stdio.h>

int main() {
    double originalPrice, newPrice;

    // Read the original price from the user
    printf("Enter the original price of the item: ");
    scanf("%lf", &originalPrice);

    // Calculate the new price by subtracting 10%
    newPrice = originalPrice - (0.10 * originalPrice);

    // Print the new price
    printf("The new price after a 10%% discount is: %.2lf\n", newPrice);

    return 0;
}