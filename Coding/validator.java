import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
@interface NotNull {
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
@interface NotBlank {
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
@interface Range {
    long min();

    long max();
}

public final class Validator {

    private Validator() {
    }

    public static List<String> validate(Object target) {
        if (target == null) {
            throw new IllegalArgumentException("target must not be null");
        }

        List<String> violations = new ArrayList<>();

        for (Class<?> type = target.getClass();
             type != null && type != Object.class;
             type = type.getSuperclass()) {

            for (Field field : type.getDeclaredFields()) {
                if (Modifier.isStatic(field.getModifiers())) {
                    continue;
                }

                field.setAccessible(true);

                try {
                    Object value = field.get(target);
                    String fieldName = field.getName();

                    if (field.isAnnotationPresent(NotNull.class) && value == null) {
                        violations.add(fieldName + ": must not be null");
                    }

                    if (field.isAnnotationPresent(NotBlank.class)
                            && (value == null
                            || (value instanceof String text && text.trim().isEmpty()))) {
                        violations.add(fieldName + ": must not be blank");
                    }

                    Range range = field.getAnnotation(Range.class);
                    if (range != null && value != null && isIntegerOrLong(field.getType())) {
                        long number = ((Number) value).longValue();

                        if (number < range.min() || number > range.max()) {
                            violations.add(fieldName + ": must be between "
                                    + range.min() + " and " + range.max());
                        }
                    }
                } catch (IllegalAccessException e) {
                    throw new IllegalStateException("Cannot access field: " + field.getName(), e);
                }
            }
        }

        Collections.sort(violations);
        return violations;
    }

    private static boolean isIntegerOrLong(Class<?> type) {
        return type == int.class
                || type == long.class
                || type == Integer.class
                || type == Long.class;
    }
}
