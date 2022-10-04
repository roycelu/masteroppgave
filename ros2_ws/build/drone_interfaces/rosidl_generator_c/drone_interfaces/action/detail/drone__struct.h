// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from drone_interfaces:action/Drone.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__ACTION__DETAIL__DRONE__STRUCT_H_
#define DRONE_INTERFACES__ACTION__DETAIL__DRONE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'pos'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in action/Drone in the package drone_interfaces.
typedef struct drone_interfaces__action__Drone_Goal
{
  rosidl_runtime_c__float__Sequence pos;
} drone_interfaces__action__Drone_Goal;

// Struct for a sequence of drone_interfaces__action__Drone_Goal.
typedef struct drone_interfaces__action__Drone_Goal__Sequence
{
  drone_interfaces__action__Drone_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__action__Drone_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'final_pos'
// already included above
// #include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in action/Drone in the package drone_interfaces.
typedef struct drone_interfaces__action__Drone_Result
{
  rosidl_runtime_c__float__Sequence final_pos;
} drone_interfaces__action__Drone_Result;

// Struct for a sequence of drone_interfaces__action__Drone_Result.
typedef struct drone_interfaces__action__Drone_Result__Sequence
{
  drone_interfaces__action__Drone_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__action__Drone_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'current_pos'
// already included above
// #include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in action/Drone in the package drone_interfaces.
typedef struct drone_interfaces__action__Drone_Feedback
{
  rosidl_runtime_c__float__Sequence current_pos;
} drone_interfaces__action__Drone_Feedback;

// Struct for a sequence of drone_interfaces__action__Drone_Feedback.
typedef struct drone_interfaces__action__Drone_Feedback__Sequence
{
  drone_interfaces__action__Drone_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__action__Drone_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "drone_interfaces/action/detail/drone__struct.h"

/// Struct defined in action/Drone in the package drone_interfaces.
typedef struct drone_interfaces__action__Drone_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  drone_interfaces__action__Drone_Goal goal;
} drone_interfaces__action__Drone_SendGoal_Request;

// Struct for a sequence of drone_interfaces__action__Drone_SendGoal_Request.
typedef struct drone_interfaces__action__Drone_SendGoal_Request__Sequence
{
  drone_interfaces__action__Drone_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__action__Drone_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/Drone in the package drone_interfaces.
typedef struct drone_interfaces__action__Drone_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} drone_interfaces__action__Drone_SendGoal_Response;

// Struct for a sequence of drone_interfaces__action__Drone_SendGoal_Response.
typedef struct drone_interfaces__action__Drone_SendGoal_Response__Sequence
{
  drone_interfaces__action__Drone_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__action__Drone_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/Drone in the package drone_interfaces.
typedef struct drone_interfaces__action__Drone_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} drone_interfaces__action__Drone_GetResult_Request;

// Struct for a sequence of drone_interfaces__action__Drone_GetResult_Request.
typedef struct drone_interfaces__action__Drone_GetResult_Request__Sequence
{
  drone_interfaces__action__Drone_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__action__Drone_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "drone_interfaces/action/detail/drone__struct.h"

/// Struct defined in action/Drone in the package drone_interfaces.
typedef struct drone_interfaces__action__Drone_GetResult_Response
{
  int8_t status;
  drone_interfaces__action__Drone_Result result;
} drone_interfaces__action__Drone_GetResult_Response;

// Struct for a sequence of drone_interfaces__action__Drone_GetResult_Response.
typedef struct drone_interfaces__action__Drone_GetResult_Response__Sequence
{
  drone_interfaces__action__Drone_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__action__Drone_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "drone_interfaces/action/detail/drone__struct.h"

/// Struct defined in action/Drone in the package drone_interfaces.
typedef struct drone_interfaces__action__Drone_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  drone_interfaces__action__Drone_Feedback feedback;
} drone_interfaces__action__Drone_FeedbackMessage;

// Struct for a sequence of drone_interfaces__action__Drone_FeedbackMessage.
typedef struct drone_interfaces__action__Drone_FeedbackMessage__Sequence
{
  drone_interfaces__action__Drone_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__action__Drone_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DRONE_INTERFACES__ACTION__DETAIL__DRONE__STRUCT_H_
