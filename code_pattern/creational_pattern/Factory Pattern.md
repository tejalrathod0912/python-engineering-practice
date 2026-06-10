## Factory Pattern

### Definition

Provides a centralized way to create objects without exposing the creation logic to the client.

### Real-World Analogy

A car factory creates different types of vehicles based on customer requests. The customer does not need to know how the car is assembled.

### When to Use

* Supporting multiple providers
* Supporting multiple file formats
* Creating different database clients
* Cloud provider integrations

### Benefits

* Simplifies object creation
* Reduces coupling
* Improves maintainability

### Production Example

Creating Azure, AWS, or GCP storage clients using a common interface.
