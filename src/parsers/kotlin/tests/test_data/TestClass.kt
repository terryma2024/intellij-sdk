/**
 * This is a test class demonstrating various Kotlin language features
 * for testing the Kotlin parser implementation.
 */

@Deprecated("For testing purposes")
class TestClass<T> {
    // Constant property
    const val MAX_COUNT = 100
    
    // Regular property
    private var count: Int = 0
    
    /**
     * A companion object with constants
     */
    companion object {
        const val DEFAULT_NAME = "test"
        const val VERSION = 1.0
    }
    
    /**
     * Primary constructor property
     */
    var name: String = ""
        private set
    
    // Different types of functions
    fun basicFunction() {
        println("Basic function")
    }
    
    /**
     * Function with parameters and return type
     */
    fun parameterizedFunction(input: String, count: Int): Boolean {
        return input.length > count
    }
    
    // Generic function
    fun <R> genericFunction(value: T): R? {
        return null
    }
    
    // Extension function
    fun String.addPrefix(): String {
        return "prefix_$this"
    }
    
    // Nested class with constants
    class NestedClass {
        const val NESTED_CONSTANT = "nested"
        
        // Nested function
        fun nestedFunction() {
            println("Nested function")
        }
    }
    
    // Data class
    data class DataItem(
        val id: Int,
        val value: String
    )
    
    // Enum class
    enum class Status {
        ACTIVE,
        INACTIVE,
        PENDING
    }
    
    // Interface
    interface TestInterface {
        fun interfaceMethod()
        val interfaceProperty: String
    }
}