// Test file for complex Java annotations
public class Annos {
    public @interface Dummy4 {
        String[] value();
    }

    @Documented
    @Retention(RetentionPolicy.RUNTIME)
    @Target({ ElementType.TYPE_USE, ElementType.TYPE_PARAMETER })
    public @interface Dummy03 {
        Dummy3[] value();
    }

    @Documented
    @Retention(RetentionPolicy.RUNTIME)
    @Target({ ElementType.TYPE_USE, ElementType.TYPE_PARAMETER })
    public @interface Dummy01 {
        Dummy1[] value();
    }

    @Documented
    @Retention(RetentionPolicy.RUNTIME)
    @Target({ ElementType.TYPE_USE, ElementType.TYPE_PARAMETER })
    @Repeatable(Dummy01.class)
    public @interface Dummy1 {
    }

    @Documented
    @Retention(RetentionPolicy.RUNTIME)
    @Target({ ElementType.TYPE_USE, ElementType.TYPE_PARAMETER })
    public @interface Dummy2 {
    }

    @Documented
    @Retention(RetentionPolicy.RUNTIME)
    @Target({ ElementType.TYPE_USE, ElementType.TYPE_PARAMETER })
    @Repeatable(Dummy03.class)
    public @interface Dummy3 {
    }

    public static @Dummy4("#1") @Dummy1 @Dummy3 <T extends @Dummy2 @Dummy3 Object> @Dummy1 @Dummy3 T @Dummy1 @Dummy3 [] foo(
            @Dummy1 T @Dummy2 @Dummy3 [] arr, @Dummy1 @Dummy3 T @Dummy1 @Dummy3... t) {
        return (@Dummy1 @Dummy3 T[]) null;
    }

    public static @Dummy4("") <@Dummy1 @Dummy2 T extends @Dummy1 @Dummy3 Object> @Dummy1 @Dummy3 T @Dummy1 @Dummy3 [] @Dummy1 @Dummy2 [] foo2(
            @Dummy1 T @Dummy2 @Dummy3 [] @Dummy1 @Dummy3 [] arr) {
        return (@Dummy1 @Dummy2 T[] @Dummy1 @Dummy2 []) null;
    }

    class Gen<T> {
    }

    class A<@Dummy1 T extends @Dummy1 Gen<@Dummy1 T>> {
    }

    public static <@Dummy3 T> void foo3(T t, Gen<@Dummy1 @Dummy3 ? super @Dummy1 @Dummy3 T> c) {
    }

    public static <@Dummy3 T> void foo33(T t, Gen<@Dummy1 @Dummy3 ?> c) {
    }

    public static <@Dummy3 T, @Dummy1 S> void foo333(T t, Gen<@Dummy1 @Dummy3 T @Dummy1 []> c) {
    }

    public static @Dummy3 <@Dummy3 T extends @Dummy3 Gen<@Dummy1 ? super @Dummy1 T>> @Dummy3 T @Dummy3 [] f(
            @Dummy3 T @Dummy3... t) {
        return (@Dummy3 T @Dummy3 []) null;
    }
}