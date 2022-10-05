// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from drone_interfaces:action/Drone.idl
// generated code does not contain a copyright notice
#include "drone_interfaces/action/detail/drone__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `pos`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
drone_interfaces__action__Drone_Goal__init(drone_interfaces__action__Drone_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // pos
  if (!rosidl_runtime_c__float__Sequence__init(&msg->pos, 0)) {
    drone_interfaces__action__Drone_Goal__fini(msg);
    return false;
  }
  return true;
}

void
drone_interfaces__action__Drone_Goal__fini(drone_interfaces__action__Drone_Goal * msg)
{
  if (!msg) {
    return;
  }
  // pos
  rosidl_runtime_c__float__Sequence__fini(&msg->pos);
}

bool
drone_interfaces__action__Drone_Goal__are_equal(const drone_interfaces__action__Drone_Goal * lhs, const drone_interfaces__action__Drone_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // pos
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->pos), &(rhs->pos)))
  {
    return false;
  }
  return true;
}

bool
drone_interfaces__action__Drone_Goal__copy(
  const drone_interfaces__action__Drone_Goal * input,
  drone_interfaces__action__Drone_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // pos
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->pos), &(output->pos)))
  {
    return false;
  }
  return true;
}

drone_interfaces__action__Drone_Goal *
drone_interfaces__action__Drone_Goal__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_Goal * msg = (drone_interfaces__action__Drone_Goal *)allocator.allocate(sizeof(drone_interfaces__action__Drone_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__action__Drone_Goal));
  bool success = drone_interfaces__action__Drone_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__action__Drone_Goal__destroy(drone_interfaces__action__Drone_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__action__Drone_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__action__Drone_Goal__Sequence__init(drone_interfaces__action__Drone_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_Goal * data = NULL;

  if (size) {
    data = (drone_interfaces__action__Drone_Goal *)allocator.zero_allocate(size, sizeof(drone_interfaces__action__Drone_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__action__Drone_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__action__Drone_Goal__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drone_interfaces__action__Drone_Goal__Sequence__fini(drone_interfaces__action__Drone_Goal__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drone_interfaces__action__Drone_Goal__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drone_interfaces__action__Drone_Goal__Sequence *
drone_interfaces__action__Drone_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_Goal__Sequence * array = (drone_interfaces__action__Drone_Goal__Sequence *)allocator.allocate(sizeof(drone_interfaces__action__Drone_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__action__Drone_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__action__Drone_Goal__Sequence__destroy(drone_interfaces__action__Drone_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__action__Drone_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__action__Drone_Goal__Sequence__are_equal(const drone_interfaces__action__Drone_Goal__Sequence * lhs, const drone_interfaces__action__Drone_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__action__Drone_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__action__Drone_Goal__Sequence__copy(
  const drone_interfaces__action__Drone_Goal__Sequence * input,
  drone_interfaces__action__Drone_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__action__Drone_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__action__Drone_Goal * data =
      (drone_interfaces__action__Drone_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__action__Drone_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__action__Drone_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__action__Drone_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `final_pos`
// already included above
// #include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
drone_interfaces__action__Drone_Result__init(drone_interfaces__action__Drone_Result * msg)
{
  if (!msg) {
    return false;
  }
  // final_pos
  if (!rosidl_runtime_c__float__Sequence__init(&msg->final_pos, 0)) {
    drone_interfaces__action__Drone_Result__fini(msg);
    return false;
  }
  return true;
}

void
drone_interfaces__action__Drone_Result__fini(drone_interfaces__action__Drone_Result * msg)
{
  if (!msg) {
    return;
  }
  // final_pos
  rosidl_runtime_c__float__Sequence__fini(&msg->final_pos);
}

bool
drone_interfaces__action__Drone_Result__are_equal(const drone_interfaces__action__Drone_Result * lhs, const drone_interfaces__action__Drone_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // final_pos
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->final_pos), &(rhs->final_pos)))
  {
    return false;
  }
  return true;
}

bool
drone_interfaces__action__Drone_Result__copy(
  const drone_interfaces__action__Drone_Result * input,
  drone_interfaces__action__Drone_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // final_pos
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->final_pos), &(output->final_pos)))
  {
    return false;
  }
  return true;
}

drone_interfaces__action__Drone_Result *
drone_interfaces__action__Drone_Result__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_Result * msg = (drone_interfaces__action__Drone_Result *)allocator.allocate(sizeof(drone_interfaces__action__Drone_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__action__Drone_Result));
  bool success = drone_interfaces__action__Drone_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__action__Drone_Result__destroy(drone_interfaces__action__Drone_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__action__Drone_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__action__Drone_Result__Sequence__init(drone_interfaces__action__Drone_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_Result * data = NULL;

  if (size) {
    data = (drone_interfaces__action__Drone_Result *)allocator.zero_allocate(size, sizeof(drone_interfaces__action__Drone_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__action__Drone_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__action__Drone_Result__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drone_interfaces__action__Drone_Result__Sequence__fini(drone_interfaces__action__Drone_Result__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drone_interfaces__action__Drone_Result__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drone_interfaces__action__Drone_Result__Sequence *
drone_interfaces__action__Drone_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_Result__Sequence * array = (drone_interfaces__action__Drone_Result__Sequence *)allocator.allocate(sizeof(drone_interfaces__action__Drone_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__action__Drone_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__action__Drone_Result__Sequence__destroy(drone_interfaces__action__Drone_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__action__Drone_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__action__Drone_Result__Sequence__are_equal(const drone_interfaces__action__Drone_Result__Sequence * lhs, const drone_interfaces__action__Drone_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__action__Drone_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__action__Drone_Result__Sequence__copy(
  const drone_interfaces__action__Drone_Result__Sequence * input,
  drone_interfaces__action__Drone_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__action__Drone_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__action__Drone_Result * data =
      (drone_interfaces__action__Drone_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__action__Drone_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__action__Drone_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__action__Drone_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `current_pos`
// already included above
// #include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
drone_interfaces__action__Drone_Feedback__init(drone_interfaces__action__Drone_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // current_pos
  if (!rosidl_runtime_c__float__Sequence__init(&msg->current_pos, 0)) {
    drone_interfaces__action__Drone_Feedback__fini(msg);
    return false;
  }
  return true;
}

void
drone_interfaces__action__Drone_Feedback__fini(drone_interfaces__action__Drone_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // current_pos
  rosidl_runtime_c__float__Sequence__fini(&msg->current_pos);
}

bool
drone_interfaces__action__Drone_Feedback__are_equal(const drone_interfaces__action__Drone_Feedback * lhs, const drone_interfaces__action__Drone_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // current_pos
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->current_pos), &(rhs->current_pos)))
  {
    return false;
  }
  return true;
}

bool
drone_interfaces__action__Drone_Feedback__copy(
  const drone_interfaces__action__Drone_Feedback * input,
  drone_interfaces__action__Drone_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // current_pos
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->current_pos), &(output->current_pos)))
  {
    return false;
  }
  return true;
}

drone_interfaces__action__Drone_Feedback *
drone_interfaces__action__Drone_Feedback__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_Feedback * msg = (drone_interfaces__action__Drone_Feedback *)allocator.allocate(sizeof(drone_interfaces__action__Drone_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__action__Drone_Feedback));
  bool success = drone_interfaces__action__Drone_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__action__Drone_Feedback__destroy(drone_interfaces__action__Drone_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__action__Drone_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__action__Drone_Feedback__Sequence__init(drone_interfaces__action__Drone_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_Feedback * data = NULL;

  if (size) {
    data = (drone_interfaces__action__Drone_Feedback *)allocator.zero_allocate(size, sizeof(drone_interfaces__action__Drone_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__action__Drone_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__action__Drone_Feedback__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drone_interfaces__action__Drone_Feedback__Sequence__fini(drone_interfaces__action__Drone_Feedback__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drone_interfaces__action__Drone_Feedback__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drone_interfaces__action__Drone_Feedback__Sequence *
drone_interfaces__action__Drone_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_Feedback__Sequence * array = (drone_interfaces__action__Drone_Feedback__Sequence *)allocator.allocate(sizeof(drone_interfaces__action__Drone_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__action__Drone_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__action__Drone_Feedback__Sequence__destroy(drone_interfaces__action__Drone_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__action__Drone_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__action__Drone_Feedback__Sequence__are_equal(const drone_interfaces__action__Drone_Feedback__Sequence * lhs, const drone_interfaces__action__Drone_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__action__Drone_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__action__Drone_Feedback__Sequence__copy(
  const drone_interfaces__action__Drone_Feedback__Sequence * input,
  drone_interfaces__action__Drone_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__action__Drone_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__action__Drone_Feedback * data =
      (drone_interfaces__action__Drone_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__action__Drone_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__action__Drone_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__action__Drone_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "drone_interfaces/action/detail/drone__functions.h"

bool
drone_interfaces__action__Drone_SendGoal_Request__init(drone_interfaces__action__Drone_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    drone_interfaces__action__Drone_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!drone_interfaces__action__Drone_Goal__init(&msg->goal)) {
    drone_interfaces__action__Drone_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
drone_interfaces__action__Drone_SendGoal_Request__fini(drone_interfaces__action__Drone_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  drone_interfaces__action__Drone_Goal__fini(&msg->goal);
}

bool
drone_interfaces__action__Drone_SendGoal_Request__are_equal(const drone_interfaces__action__Drone_SendGoal_Request * lhs, const drone_interfaces__action__Drone_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!drone_interfaces__action__Drone_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
drone_interfaces__action__Drone_SendGoal_Request__copy(
  const drone_interfaces__action__Drone_SendGoal_Request * input,
  drone_interfaces__action__Drone_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!drone_interfaces__action__Drone_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

drone_interfaces__action__Drone_SendGoal_Request *
drone_interfaces__action__Drone_SendGoal_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_SendGoal_Request * msg = (drone_interfaces__action__Drone_SendGoal_Request *)allocator.allocate(sizeof(drone_interfaces__action__Drone_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__action__Drone_SendGoal_Request));
  bool success = drone_interfaces__action__Drone_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__action__Drone_SendGoal_Request__destroy(drone_interfaces__action__Drone_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__action__Drone_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__action__Drone_SendGoal_Request__Sequence__init(drone_interfaces__action__Drone_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_SendGoal_Request * data = NULL;

  if (size) {
    data = (drone_interfaces__action__Drone_SendGoal_Request *)allocator.zero_allocate(size, sizeof(drone_interfaces__action__Drone_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__action__Drone_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__action__Drone_SendGoal_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drone_interfaces__action__Drone_SendGoal_Request__Sequence__fini(drone_interfaces__action__Drone_SendGoal_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drone_interfaces__action__Drone_SendGoal_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drone_interfaces__action__Drone_SendGoal_Request__Sequence *
drone_interfaces__action__Drone_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_SendGoal_Request__Sequence * array = (drone_interfaces__action__Drone_SendGoal_Request__Sequence *)allocator.allocate(sizeof(drone_interfaces__action__Drone_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__action__Drone_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__action__Drone_SendGoal_Request__Sequence__destroy(drone_interfaces__action__Drone_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__action__Drone_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__action__Drone_SendGoal_Request__Sequence__are_equal(const drone_interfaces__action__Drone_SendGoal_Request__Sequence * lhs, const drone_interfaces__action__Drone_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__action__Drone_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__action__Drone_SendGoal_Request__Sequence__copy(
  const drone_interfaces__action__Drone_SendGoal_Request__Sequence * input,
  drone_interfaces__action__Drone_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__action__Drone_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__action__Drone_SendGoal_Request * data =
      (drone_interfaces__action__Drone_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__action__Drone_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__action__Drone_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__action__Drone_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
drone_interfaces__action__Drone_SendGoal_Response__init(drone_interfaces__action__Drone_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    drone_interfaces__action__Drone_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
drone_interfaces__action__Drone_SendGoal_Response__fini(drone_interfaces__action__Drone_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
drone_interfaces__action__Drone_SendGoal_Response__are_equal(const drone_interfaces__action__Drone_SendGoal_Response * lhs, const drone_interfaces__action__Drone_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
drone_interfaces__action__Drone_SendGoal_Response__copy(
  const drone_interfaces__action__Drone_SendGoal_Response * input,
  drone_interfaces__action__Drone_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

drone_interfaces__action__Drone_SendGoal_Response *
drone_interfaces__action__Drone_SendGoal_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_SendGoal_Response * msg = (drone_interfaces__action__Drone_SendGoal_Response *)allocator.allocate(sizeof(drone_interfaces__action__Drone_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__action__Drone_SendGoal_Response));
  bool success = drone_interfaces__action__Drone_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__action__Drone_SendGoal_Response__destroy(drone_interfaces__action__Drone_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__action__Drone_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__action__Drone_SendGoal_Response__Sequence__init(drone_interfaces__action__Drone_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_SendGoal_Response * data = NULL;

  if (size) {
    data = (drone_interfaces__action__Drone_SendGoal_Response *)allocator.zero_allocate(size, sizeof(drone_interfaces__action__Drone_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__action__Drone_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__action__Drone_SendGoal_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drone_interfaces__action__Drone_SendGoal_Response__Sequence__fini(drone_interfaces__action__Drone_SendGoal_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drone_interfaces__action__Drone_SendGoal_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drone_interfaces__action__Drone_SendGoal_Response__Sequence *
drone_interfaces__action__Drone_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_SendGoal_Response__Sequence * array = (drone_interfaces__action__Drone_SendGoal_Response__Sequence *)allocator.allocate(sizeof(drone_interfaces__action__Drone_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__action__Drone_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__action__Drone_SendGoal_Response__Sequence__destroy(drone_interfaces__action__Drone_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__action__Drone_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__action__Drone_SendGoal_Response__Sequence__are_equal(const drone_interfaces__action__Drone_SendGoal_Response__Sequence * lhs, const drone_interfaces__action__Drone_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__action__Drone_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__action__Drone_SendGoal_Response__Sequence__copy(
  const drone_interfaces__action__Drone_SendGoal_Response__Sequence * input,
  drone_interfaces__action__Drone_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__action__Drone_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__action__Drone_SendGoal_Response * data =
      (drone_interfaces__action__Drone_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__action__Drone_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__action__Drone_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__action__Drone_SendGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
drone_interfaces__action__Drone_GetResult_Request__init(drone_interfaces__action__Drone_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    drone_interfaces__action__Drone_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
drone_interfaces__action__Drone_GetResult_Request__fini(drone_interfaces__action__Drone_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
drone_interfaces__action__Drone_GetResult_Request__are_equal(const drone_interfaces__action__Drone_GetResult_Request * lhs, const drone_interfaces__action__Drone_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
drone_interfaces__action__Drone_GetResult_Request__copy(
  const drone_interfaces__action__Drone_GetResult_Request * input,
  drone_interfaces__action__Drone_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

drone_interfaces__action__Drone_GetResult_Request *
drone_interfaces__action__Drone_GetResult_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_GetResult_Request * msg = (drone_interfaces__action__Drone_GetResult_Request *)allocator.allocate(sizeof(drone_interfaces__action__Drone_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__action__Drone_GetResult_Request));
  bool success = drone_interfaces__action__Drone_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__action__Drone_GetResult_Request__destroy(drone_interfaces__action__Drone_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__action__Drone_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__action__Drone_GetResult_Request__Sequence__init(drone_interfaces__action__Drone_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_GetResult_Request * data = NULL;

  if (size) {
    data = (drone_interfaces__action__Drone_GetResult_Request *)allocator.zero_allocate(size, sizeof(drone_interfaces__action__Drone_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__action__Drone_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__action__Drone_GetResult_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drone_interfaces__action__Drone_GetResult_Request__Sequence__fini(drone_interfaces__action__Drone_GetResult_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drone_interfaces__action__Drone_GetResult_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drone_interfaces__action__Drone_GetResult_Request__Sequence *
drone_interfaces__action__Drone_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_GetResult_Request__Sequence * array = (drone_interfaces__action__Drone_GetResult_Request__Sequence *)allocator.allocate(sizeof(drone_interfaces__action__Drone_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__action__Drone_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__action__Drone_GetResult_Request__Sequence__destroy(drone_interfaces__action__Drone_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__action__Drone_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__action__Drone_GetResult_Request__Sequence__are_equal(const drone_interfaces__action__Drone_GetResult_Request__Sequence * lhs, const drone_interfaces__action__Drone_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__action__Drone_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__action__Drone_GetResult_Request__Sequence__copy(
  const drone_interfaces__action__Drone_GetResult_Request__Sequence * input,
  drone_interfaces__action__Drone_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__action__Drone_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__action__Drone_GetResult_Request * data =
      (drone_interfaces__action__Drone_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__action__Drone_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__action__Drone_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__action__Drone_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "drone_interfaces/action/detail/drone__functions.h"

bool
drone_interfaces__action__Drone_GetResult_Response__init(drone_interfaces__action__Drone_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!drone_interfaces__action__Drone_Result__init(&msg->result)) {
    drone_interfaces__action__Drone_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
drone_interfaces__action__Drone_GetResult_Response__fini(drone_interfaces__action__Drone_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  drone_interfaces__action__Drone_Result__fini(&msg->result);
}

bool
drone_interfaces__action__Drone_GetResult_Response__are_equal(const drone_interfaces__action__Drone_GetResult_Response * lhs, const drone_interfaces__action__Drone_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!drone_interfaces__action__Drone_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
drone_interfaces__action__Drone_GetResult_Response__copy(
  const drone_interfaces__action__Drone_GetResult_Response * input,
  drone_interfaces__action__Drone_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!drone_interfaces__action__Drone_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

drone_interfaces__action__Drone_GetResult_Response *
drone_interfaces__action__Drone_GetResult_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_GetResult_Response * msg = (drone_interfaces__action__Drone_GetResult_Response *)allocator.allocate(sizeof(drone_interfaces__action__Drone_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__action__Drone_GetResult_Response));
  bool success = drone_interfaces__action__Drone_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__action__Drone_GetResult_Response__destroy(drone_interfaces__action__Drone_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__action__Drone_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__action__Drone_GetResult_Response__Sequence__init(drone_interfaces__action__Drone_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_GetResult_Response * data = NULL;

  if (size) {
    data = (drone_interfaces__action__Drone_GetResult_Response *)allocator.zero_allocate(size, sizeof(drone_interfaces__action__Drone_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__action__Drone_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__action__Drone_GetResult_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drone_interfaces__action__Drone_GetResult_Response__Sequence__fini(drone_interfaces__action__Drone_GetResult_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drone_interfaces__action__Drone_GetResult_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drone_interfaces__action__Drone_GetResult_Response__Sequence *
drone_interfaces__action__Drone_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_GetResult_Response__Sequence * array = (drone_interfaces__action__Drone_GetResult_Response__Sequence *)allocator.allocate(sizeof(drone_interfaces__action__Drone_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__action__Drone_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__action__Drone_GetResult_Response__Sequence__destroy(drone_interfaces__action__Drone_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__action__Drone_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__action__Drone_GetResult_Response__Sequence__are_equal(const drone_interfaces__action__Drone_GetResult_Response__Sequence * lhs, const drone_interfaces__action__Drone_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__action__Drone_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__action__Drone_GetResult_Response__Sequence__copy(
  const drone_interfaces__action__Drone_GetResult_Response__Sequence * input,
  drone_interfaces__action__Drone_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__action__Drone_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__action__Drone_GetResult_Response * data =
      (drone_interfaces__action__Drone_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__action__Drone_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__action__Drone_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__action__Drone_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "drone_interfaces/action/detail/drone__functions.h"

bool
drone_interfaces__action__Drone_FeedbackMessage__init(drone_interfaces__action__Drone_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    drone_interfaces__action__Drone_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!drone_interfaces__action__Drone_Feedback__init(&msg->feedback)) {
    drone_interfaces__action__Drone_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
drone_interfaces__action__Drone_FeedbackMessage__fini(drone_interfaces__action__Drone_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  drone_interfaces__action__Drone_Feedback__fini(&msg->feedback);
}

bool
drone_interfaces__action__Drone_FeedbackMessage__are_equal(const drone_interfaces__action__Drone_FeedbackMessage * lhs, const drone_interfaces__action__Drone_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!drone_interfaces__action__Drone_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
drone_interfaces__action__Drone_FeedbackMessage__copy(
  const drone_interfaces__action__Drone_FeedbackMessage * input,
  drone_interfaces__action__Drone_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!drone_interfaces__action__Drone_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

drone_interfaces__action__Drone_FeedbackMessage *
drone_interfaces__action__Drone_FeedbackMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_FeedbackMessage * msg = (drone_interfaces__action__Drone_FeedbackMessage *)allocator.allocate(sizeof(drone_interfaces__action__Drone_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__action__Drone_FeedbackMessage));
  bool success = drone_interfaces__action__Drone_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__action__Drone_FeedbackMessage__destroy(drone_interfaces__action__Drone_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__action__Drone_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__action__Drone_FeedbackMessage__Sequence__init(drone_interfaces__action__Drone_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_FeedbackMessage * data = NULL;

  if (size) {
    data = (drone_interfaces__action__Drone_FeedbackMessage *)allocator.zero_allocate(size, sizeof(drone_interfaces__action__Drone_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__action__Drone_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__action__Drone_FeedbackMessage__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drone_interfaces__action__Drone_FeedbackMessage__Sequence__fini(drone_interfaces__action__Drone_FeedbackMessage__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drone_interfaces__action__Drone_FeedbackMessage__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drone_interfaces__action__Drone_FeedbackMessage__Sequence *
drone_interfaces__action__Drone_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__action__Drone_FeedbackMessage__Sequence * array = (drone_interfaces__action__Drone_FeedbackMessage__Sequence *)allocator.allocate(sizeof(drone_interfaces__action__Drone_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__action__Drone_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__action__Drone_FeedbackMessage__Sequence__destroy(drone_interfaces__action__Drone_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__action__Drone_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__action__Drone_FeedbackMessage__Sequence__are_equal(const drone_interfaces__action__Drone_FeedbackMessage__Sequence * lhs, const drone_interfaces__action__Drone_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__action__Drone_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__action__Drone_FeedbackMessage__Sequence__copy(
  const drone_interfaces__action__Drone_FeedbackMessage__Sequence * input,
  drone_interfaces__action__Drone_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__action__Drone_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__action__Drone_FeedbackMessage * data =
      (drone_interfaces__action__Drone_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__action__Drone_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__action__Drone_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__action__Drone_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
