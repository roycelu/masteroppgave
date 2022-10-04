// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from drone_interfaces:action/Drone.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "drone_interfaces/action/detail/drone__struct.h"
#include "drone_interfaces/action/detail/drone__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace drone_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Drone_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Drone_Goal_type_support_ids_t;

static const _Drone_Goal_type_support_ids_t _Drone_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Drone_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Drone_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Drone_Goal_type_support_symbol_names_t _Drone_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_interfaces, action, Drone_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, action, Drone_Goal)),
  }
};

typedef struct _Drone_Goal_type_support_data_t
{
  void * data[2];
} _Drone_Goal_type_support_data_t;

static _Drone_Goal_type_support_data_t _Drone_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Drone_Goal_message_typesupport_map = {
  2,
  "drone_interfaces",
  &_Drone_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_Drone_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_Drone_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Drone_Goal_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Drone_Goal_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace drone_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, drone_interfaces, action, Drone_Goal)() {
  return &::drone_interfaces::action::rosidl_typesupport_c::Drone_Goal_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace drone_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Drone_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Drone_Result_type_support_ids_t;

static const _Drone_Result_type_support_ids_t _Drone_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Drone_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Drone_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Drone_Result_type_support_symbol_names_t _Drone_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_interfaces, action, Drone_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, action, Drone_Result)),
  }
};

typedef struct _Drone_Result_type_support_data_t
{
  void * data[2];
} _Drone_Result_type_support_data_t;

static _Drone_Result_type_support_data_t _Drone_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Drone_Result_message_typesupport_map = {
  2,
  "drone_interfaces",
  &_Drone_Result_message_typesupport_ids.typesupport_identifier[0],
  &_Drone_Result_message_typesupport_symbol_names.symbol_name[0],
  &_Drone_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Drone_Result_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Drone_Result_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace drone_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, drone_interfaces, action, Drone_Result)() {
  return &::drone_interfaces::action::rosidl_typesupport_c::Drone_Result_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace drone_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Drone_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Drone_Feedback_type_support_ids_t;

static const _Drone_Feedback_type_support_ids_t _Drone_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Drone_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Drone_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Drone_Feedback_type_support_symbol_names_t _Drone_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_interfaces, action, Drone_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, action, Drone_Feedback)),
  }
};

typedef struct _Drone_Feedback_type_support_data_t
{
  void * data[2];
} _Drone_Feedback_type_support_data_t;

static _Drone_Feedback_type_support_data_t _Drone_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Drone_Feedback_message_typesupport_map = {
  2,
  "drone_interfaces",
  &_Drone_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_Drone_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_Drone_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Drone_Feedback_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Drone_Feedback_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace drone_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, drone_interfaces, action, Drone_Feedback)() {
  return &::drone_interfaces::action::rosidl_typesupport_c::Drone_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace drone_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Drone_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Drone_SendGoal_Request_type_support_ids_t;

static const _Drone_SendGoal_Request_type_support_ids_t _Drone_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Drone_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Drone_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Drone_SendGoal_Request_type_support_symbol_names_t _Drone_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_interfaces, action, Drone_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, action, Drone_SendGoal_Request)),
  }
};

typedef struct _Drone_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _Drone_SendGoal_Request_type_support_data_t;

static _Drone_SendGoal_Request_type_support_data_t _Drone_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Drone_SendGoal_Request_message_typesupport_map = {
  2,
  "drone_interfaces",
  &_Drone_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_Drone_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_Drone_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Drone_SendGoal_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Drone_SendGoal_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace drone_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, drone_interfaces, action, Drone_SendGoal_Request)() {
  return &::drone_interfaces::action::rosidl_typesupport_c::Drone_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace drone_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Drone_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Drone_SendGoal_Response_type_support_ids_t;

static const _Drone_SendGoal_Response_type_support_ids_t _Drone_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Drone_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Drone_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Drone_SendGoal_Response_type_support_symbol_names_t _Drone_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_interfaces, action, Drone_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, action, Drone_SendGoal_Response)),
  }
};

typedef struct _Drone_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _Drone_SendGoal_Response_type_support_data_t;

static _Drone_SendGoal_Response_type_support_data_t _Drone_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Drone_SendGoal_Response_message_typesupport_map = {
  2,
  "drone_interfaces",
  &_Drone_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_Drone_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_Drone_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Drone_SendGoal_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Drone_SendGoal_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace drone_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, drone_interfaces, action, Drone_SendGoal_Response)() {
  return &::drone_interfaces::action::rosidl_typesupport_c::Drone_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace drone_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Drone_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Drone_SendGoal_type_support_ids_t;

static const _Drone_SendGoal_type_support_ids_t _Drone_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Drone_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Drone_SendGoal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Drone_SendGoal_type_support_symbol_names_t _Drone_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_interfaces, action, Drone_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, action, Drone_SendGoal)),
  }
};

typedef struct _Drone_SendGoal_type_support_data_t
{
  void * data[2];
} _Drone_SendGoal_type_support_data_t;

static _Drone_SendGoal_type_support_data_t _Drone_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Drone_SendGoal_service_typesupport_map = {
  2,
  "drone_interfaces",
  &_Drone_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_Drone_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_Drone_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t Drone_SendGoal_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Drone_SendGoal_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace drone_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, drone_interfaces, action, Drone_SendGoal)() {
  return &::drone_interfaces::action::rosidl_typesupport_c::Drone_SendGoal_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace drone_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Drone_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Drone_GetResult_Request_type_support_ids_t;

static const _Drone_GetResult_Request_type_support_ids_t _Drone_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Drone_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Drone_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Drone_GetResult_Request_type_support_symbol_names_t _Drone_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_interfaces, action, Drone_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, action, Drone_GetResult_Request)),
  }
};

typedef struct _Drone_GetResult_Request_type_support_data_t
{
  void * data[2];
} _Drone_GetResult_Request_type_support_data_t;

static _Drone_GetResult_Request_type_support_data_t _Drone_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Drone_GetResult_Request_message_typesupport_map = {
  2,
  "drone_interfaces",
  &_Drone_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_Drone_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_Drone_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Drone_GetResult_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Drone_GetResult_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace drone_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, drone_interfaces, action, Drone_GetResult_Request)() {
  return &::drone_interfaces::action::rosidl_typesupport_c::Drone_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace drone_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Drone_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Drone_GetResult_Response_type_support_ids_t;

static const _Drone_GetResult_Response_type_support_ids_t _Drone_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Drone_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Drone_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Drone_GetResult_Response_type_support_symbol_names_t _Drone_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_interfaces, action, Drone_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, action, Drone_GetResult_Response)),
  }
};

typedef struct _Drone_GetResult_Response_type_support_data_t
{
  void * data[2];
} _Drone_GetResult_Response_type_support_data_t;

static _Drone_GetResult_Response_type_support_data_t _Drone_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Drone_GetResult_Response_message_typesupport_map = {
  2,
  "drone_interfaces",
  &_Drone_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_Drone_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_Drone_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Drone_GetResult_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Drone_GetResult_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace drone_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, drone_interfaces, action, Drone_GetResult_Response)() {
  return &::drone_interfaces::action::rosidl_typesupport_c::Drone_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace drone_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Drone_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Drone_GetResult_type_support_ids_t;

static const _Drone_GetResult_type_support_ids_t _Drone_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Drone_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Drone_GetResult_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Drone_GetResult_type_support_symbol_names_t _Drone_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_interfaces, action, Drone_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, action, Drone_GetResult)),
  }
};

typedef struct _Drone_GetResult_type_support_data_t
{
  void * data[2];
} _Drone_GetResult_type_support_data_t;

static _Drone_GetResult_type_support_data_t _Drone_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Drone_GetResult_service_typesupport_map = {
  2,
  "drone_interfaces",
  &_Drone_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_Drone_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_Drone_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t Drone_GetResult_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Drone_GetResult_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace drone_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, drone_interfaces, action, Drone_GetResult)() {
  return &::drone_interfaces::action::rosidl_typesupport_c::Drone_GetResult_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__struct.h"
// already included above
// #include "drone_interfaces/action/detail/drone__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace drone_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Drone_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Drone_FeedbackMessage_type_support_ids_t;

static const _Drone_FeedbackMessage_type_support_ids_t _Drone_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Drone_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Drone_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Drone_FeedbackMessage_type_support_symbol_names_t _Drone_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_interfaces, action, Drone_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, action, Drone_FeedbackMessage)),
  }
};

typedef struct _Drone_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _Drone_FeedbackMessage_type_support_data_t;

static _Drone_FeedbackMessage_type_support_data_t _Drone_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Drone_FeedbackMessage_message_typesupport_map = {
  2,
  "drone_interfaces",
  &_Drone_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_Drone_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_Drone_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Drone_FeedbackMessage_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Drone_FeedbackMessage_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace drone_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, drone_interfaces, action, Drone_FeedbackMessage)() {
  return &::drone_interfaces::action::rosidl_typesupport_c::Drone_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

#include "action_msgs/msg/goal_status_array.h"
#include "action_msgs/srv/cancel_goal.h"
#include "drone_interfaces/action/drone.h"
// already included above
// #include "drone_interfaces/action/detail/drone__type_support.h"

static rosidl_action_type_support_t _drone_interfaces__action__Drone__typesupport_c;

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(
  rosidl_typesupport_c, drone_interfaces, action, Drone)()
{
  // Thread-safe by always writing the same values to the static struct
  _drone_interfaces__action__Drone__typesupport_c.goal_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, drone_interfaces, action, Drone_SendGoal)();
  _drone_interfaces__action__Drone__typesupport_c.result_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, drone_interfaces, action, Drone_GetResult)();
  _drone_interfaces__action__Drone__typesupport_c.cancel_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, srv, CancelGoal)();
  _drone_interfaces__action__Drone__typesupport_c.feedback_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, drone_interfaces, action, Drone_FeedbackMessage)();
  _drone_interfaces__action__Drone__typesupport_c.status_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, msg, GoalStatusArray)();

  return &_drone_interfaces__action__Drone__typesupport_c;
}

#ifdef __cplusplus
}
#endif
