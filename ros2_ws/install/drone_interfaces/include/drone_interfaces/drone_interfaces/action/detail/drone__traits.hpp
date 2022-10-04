// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from drone_interfaces:action/Drone.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__ACTION__DETAIL__DRONE__TRAITS_HPP_
#define DRONE_INTERFACES__ACTION__DETAIL__DRONE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "drone_interfaces/action/detail/drone__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace drone_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Drone_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: pos
  {
    if (msg.pos.size() == 0) {
      out << "pos: []";
    } else {
      out << "pos: [";
      size_t pending_items = msg.pos.size();
      for (auto item : msg.pos) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Drone_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: pos
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.pos.size() == 0) {
      out << "pos: []\n";
    } else {
      out << "pos:\n";
      for (auto item : msg.pos) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Drone_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace drone_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use drone_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const drone_interfaces::action::Drone_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::action::Drone_Goal & msg)
{
  return drone_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::action::Drone_Goal>()
{
  return "drone_interfaces::action::Drone_Goal";
}

template<>
inline const char * name<drone_interfaces::action::Drone_Goal>()
{
  return "drone_interfaces/action/Drone_Goal";
}

template<>
struct has_fixed_size<drone_interfaces::action::Drone_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<drone_interfaces::action::Drone_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<drone_interfaces::action::Drone_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace drone_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Drone_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: final_pos
  {
    if (msg.final_pos.size() == 0) {
      out << "final_pos: []";
    } else {
      out << "final_pos: [";
      size_t pending_items = msg.final_pos.size();
      for (auto item : msg.final_pos) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Drone_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: final_pos
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.final_pos.size() == 0) {
      out << "final_pos: []\n";
    } else {
      out << "final_pos:\n";
      for (auto item : msg.final_pos) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Drone_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace drone_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use drone_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const drone_interfaces::action::Drone_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::action::Drone_Result & msg)
{
  return drone_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::action::Drone_Result>()
{
  return "drone_interfaces::action::Drone_Result";
}

template<>
inline const char * name<drone_interfaces::action::Drone_Result>()
{
  return "drone_interfaces/action/Drone_Result";
}

template<>
struct has_fixed_size<drone_interfaces::action::Drone_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<drone_interfaces::action::Drone_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<drone_interfaces::action::Drone_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace drone_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Drone_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: current_pos
  {
    if (msg.current_pos.size() == 0) {
      out << "current_pos: []";
    } else {
      out << "current_pos: [";
      size_t pending_items = msg.current_pos.size();
      for (auto item : msg.current_pos) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Drone_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: current_pos
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.current_pos.size() == 0) {
      out << "current_pos: []\n";
    } else {
      out << "current_pos:\n";
      for (auto item : msg.current_pos) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Drone_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace drone_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use drone_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const drone_interfaces::action::Drone_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::action::Drone_Feedback & msg)
{
  return drone_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::action::Drone_Feedback>()
{
  return "drone_interfaces::action::Drone_Feedback";
}

template<>
inline const char * name<drone_interfaces::action::Drone_Feedback>()
{
  return "drone_interfaces/action/Drone_Feedback";
}

template<>
struct has_fixed_size<drone_interfaces::action::Drone_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<drone_interfaces::action::Drone_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<drone_interfaces::action::Drone_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "drone_interfaces/action/detail/drone__traits.hpp"

namespace drone_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Drone_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Drone_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Drone_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace drone_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use drone_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const drone_interfaces::action::Drone_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::action::Drone_SendGoal_Request & msg)
{
  return drone_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::action::Drone_SendGoal_Request>()
{
  return "drone_interfaces::action::Drone_SendGoal_Request";
}

template<>
inline const char * name<drone_interfaces::action::Drone_SendGoal_Request>()
{
  return "drone_interfaces/action/Drone_SendGoal_Request";
}

template<>
struct has_fixed_size<drone_interfaces::action::Drone_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<drone_interfaces::action::Drone_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<drone_interfaces::action::Drone_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<drone_interfaces::action::Drone_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<drone_interfaces::action::Drone_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace drone_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Drone_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Drone_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Drone_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace drone_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use drone_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const drone_interfaces::action::Drone_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::action::Drone_SendGoal_Response & msg)
{
  return drone_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::action::Drone_SendGoal_Response>()
{
  return "drone_interfaces::action::Drone_SendGoal_Response";
}

template<>
inline const char * name<drone_interfaces::action::Drone_SendGoal_Response>()
{
  return "drone_interfaces/action/Drone_SendGoal_Response";
}

template<>
struct has_fixed_size<drone_interfaces::action::Drone_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<drone_interfaces::action::Drone_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<drone_interfaces::action::Drone_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<drone_interfaces::action::Drone_SendGoal>()
{
  return "drone_interfaces::action::Drone_SendGoal";
}

template<>
inline const char * name<drone_interfaces::action::Drone_SendGoal>()
{
  return "drone_interfaces/action/Drone_SendGoal";
}

template<>
struct has_fixed_size<drone_interfaces::action::Drone_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<drone_interfaces::action::Drone_SendGoal_Request>::value &&
    has_fixed_size<drone_interfaces::action::Drone_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<drone_interfaces::action::Drone_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<drone_interfaces::action::Drone_SendGoal_Request>::value &&
    has_bounded_size<drone_interfaces::action::Drone_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<drone_interfaces::action::Drone_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<drone_interfaces::action::Drone_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<drone_interfaces::action::Drone_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace drone_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Drone_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Drone_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Drone_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace drone_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use drone_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const drone_interfaces::action::Drone_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::action::Drone_GetResult_Request & msg)
{
  return drone_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::action::Drone_GetResult_Request>()
{
  return "drone_interfaces::action::Drone_GetResult_Request";
}

template<>
inline const char * name<drone_interfaces::action::Drone_GetResult_Request>()
{
  return "drone_interfaces/action/Drone_GetResult_Request";
}

template<>
struct has_fixed_size<drone_interfaces::action::Drone_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<drone_interfaces::action::Drone_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<drone_interfaces::action::Drone_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "drone_interfaces/action/detail/drone__traits.hpp"

namespace drone_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Drone_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Drone_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Drone_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace drone_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use drone_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const drone_interfaces::action::Drone_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::action::Drone_GetResult_Response & msg)
{
  return drone_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::action::Drone_GetResult_Response>()
{
  return "drone_interfaces::action::Drone_GetResult_Response";
}

template<>
inline const char * name<drone_interfaces::action::Drone_GetResult_Response>()
{
  return "drone_interfaces/action/Drone_GetResult_Response";
}

template<>
struct has_fixed_size<drone_interfaces::action::Drone_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<drone_interfaces::action::Drone_Result>::value> {};

template<>
struct has_bounded_size<drone_interfaces::action::Drone_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<drone_interfaces::action::Drone_Result>::value> {};

template<>
struct is_message<drone_interfaces::action::Drone_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<drone_interfaces::action::Drone_GetResult>()
{
  return "drone_interfaces::action::Drone_GetResult";
}

template<>
inline const char * name<drone_interfaces::action::Drone_GetResult>()
{
  return "drone_interfaces/action/Drone_GetResult";
}

template<>
struct has_fixed_size<drone_interfaces::action::Drone_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<drone_interfaces::action::Drone_GetResult_Request>::value &&
    has_fixed_size<drone_interfaces::action::Drone_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<drone_interfaces::action::Drone_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<drone_interfaces::action::Drone_GetResult_Request>::value &&
    has_bounded_size<drone_interfaces::action::Drone_GetResult_Response>::value
  >
{
};

template<>
struct is_service<drone_interfaces::action::Drone_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<drone_interfaces::action::Drone_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<drone_interfaces::action::Drone_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "drone_interfaces/action/detail/drone__traits.hpp"

namespace drone_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Drone_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Drone_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Drone_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace drone_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use drone_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const drone_interfaces::action::Drone_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::action::Drone_FeedbackMessage & msg)
{
  return drone_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::action::Drone_FeedbackMessage>()
{
  return "drone_interfaces::action::Drone_FeedbackMessage";
}

template<>
inline const char * name<drone_interfaces::action::Drone_FeedbackMessage>()
{
  return "drone_interfaces/action/Drone_FeedbackMessage";
}

template<>
struct has_fixed_size<drone_interfaces::action::Drone_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<drone_interfaces::action::Drone_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<drone_interfaces::action::Drone_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<drone_interfaces::action::Drone_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<drone_interfaces::action::Drone_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<drone_interfaces::action::Drone>
  : std::true_type
{
};

template<>
struct is_action_goal<drone_interfaces::action::Drone_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<drone_interfaces::action::Drone_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<drone_interfaces::action::Drone_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // DRONE_INTERFACES__ACTION__DETAIL__DRONE__TRAITS_HPP_
