/**
 * Test file containing only an extension function
 */
class TestExtensions {
    // Extension function
    fun String.addPrefix(): String {
        return "prefix_$this"
    }

    // Int extension function
    fun Int.double(): Int {
        return this * 2
    }
}