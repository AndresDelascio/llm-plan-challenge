# Inventory reservation during order processing

## Brief

Sell from a single shared stock count without accepting more units than exist. When payment declines or times out, release the reserved units within five minutes. A gateway timeout can leave payment state unknown.

## Implementation

1. Reserve stock with a single atomic decrement conditioned on sufficient stock (decrement only if the current stock covers the quantity). If it fails, reject the order and do not call the gateway.
2. Once the decrement succeeds, record a reservation ID and its creation timestamp before calling the gateway.
3. Use a sandbox payment gateway. Test two concurrent shoppers against one remaining unit and a gateway that never returns a result.
4. Release stock when the gateway returns an explicit decline.
5. When the gateway times out, automatically expire the reservation and release its stock within five minutes of the timeout. Make the release exactly-once, so a reservation's units are never returned to stock twice (for example, by a decline and an expiry both firing).
6. Never fulfil against an expired reservation. If a payment success arrives after the reservation has expired, void or refund that payment.
