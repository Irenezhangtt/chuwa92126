# Java OOP Homework 1

## Question 1
Method overloading means defining multiple methods with the same name but different parameter lists in the same class. It is resolved by the compiler, so it is compile-time (static) polymorphism.

Method overriding means that a subclass provides a new implementation of an inherited method with the same signature. It is chosen at runtime based on the actual object type, so it is runtime (dynamic) polymorphism.

## Question 2
Output:

Bark!

Although `a` has the reference type `Animal`, it refers to a `Dog` object. Java uses runtime polymorphism for overridden methods, so it calls the `Dog` version of `makeSound()`.

## Question 3
Java does not allow a class to extend multiple classes because it can cause ambiguity. The Diamond Problem happens when two parent classes inherit the same method from one common ancestor, and a child class inherits from both parents. Java would not know which version of the method to use.

Java solves this by allowing a class to extend only one class. A class can implement multiple interfaces instead. If interfaces have conflicting default methods, the class must override the method and choose the behavior explicitly.

## Question 4
The code will not compile. `Shape` is an abstract class, so it cannot be instantiated with `new Shape()`.

To fix it, create a concrete subclass of `Shape` that implements `getArea()`, then instantiate that subclass.

## Question 5
An abstract class can contain instance fields, constructors, abstract methods, and concrete methods. A class can extend only one abstract class.

An interface mainly defines a contract that classes agree to follow. A class can implement multiple interfaces. Interfaces can have default and static methods, but they do not have normal instance state like an abstract class.

For example, `Flyable` is a good interface because many unrelated classes, such as `Bird`, `Airplane`, and `Drone`, can implement the ability to fly.

## Question 6
Output:

Animal eating
Meow!

`Animal a = new Cat()` is upcasting: a `Cat` object is stored in an `Animal` reference. The `eat()` method works because it belongs to `Animal`.

`a.meow()` does not compile because the reference type is `Animal`, which does not declare `meow()`.

`Cat c = (Cat) a` is downcasting. It converts the `Animal` reference back to a `Cat` reference after checking `a instanceof Cat`. Then `c.meow()` can be called.

## Question 7
When overriding `equals()`, it should be reflexive, symmetric, transitive, consistent, and return `false` when compared with `null`. It should compare the fields that define whether two objects are logically equal.

If two objects are equal according to `equals()`, they must return the same value from `hashCode()`. This is required for hash-based collections such as `HashMap` and `HashSet`. Otherwise, equal objects may be stored or searched for incorrectly.

## Question 8
A shallow copy copies the object but shares references to nested objects. If a `Person` object has an `Address address` field, both the original and copied `Person` refer to the same `Address`. Changing the address through one person changes it for both.

A deep copy creates a new copy of the nested `Address` object too. The copied `Person` has a separate address, so changing one address does not change the other.

## Question 9
Output:

Taking off from Flyable

Both `Flyable` and `Swimmable` define a default `takeOff()` method, which creates a conflict. `Duck` must override `takeOff()` to resolve that conflict.

Inside the overridden method, `Flyable.super.takeOff()` explicitly calls the default method from `Flyable`. Therefore, the Flyable message is printed.

## Question 10
- Method A is valid because it has three parameters instead of two.
- Method B is valid because it uses `double, double` instead of `int, int`.
- Method C is not valid because it has the same method name and parameter types as the original method. Changing only the return type does not create an overload.
- Method D is not valid because changing the access modifier and parameter variable names does not change the method signature. It still has `calculate(int, int)`.
