## Command Pattern

### Definition

Encapsulates a request as an object.

### Real-World Analogy

A restaurant waiter takes your order and passes it to the kitchen without needing to know how the food is prepared.

### When to Use

* Task scheduling
* Job queues
* Undo/redo systems

### Benefits

* Decouples sender from receiver
* Improves flexibility
* Simplifies request management

### Production Example

Background job processing systems such as Celery.