// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from drone_interfaces:action/Drone.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__ACTION__DETAIL__DRONE__BUILDER_HPP_
#define DRONE_INTERFACES__ACTION__DETAIL__DRONE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "drone_interfaces/action/detail/drone__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace drone_interfaces
{

namespace action
{

namespace builder
{

class Init_Drone_Goal_pos
{
public:
  Init_Drone_Goal_pos()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::drone_interfaces::action::Drone_Goal pos(::drone_interfaces::action::Drone_Goal::_pos_type arg)
  {
    msg_.pos = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::action::Drone_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::action::Drone_Goal>()
{
  return drone_interfaces::action::builder::Init_Drone_Goal_pos();
}

}  // namespace drone_interfaces


namespace drone_interfaces
{

namespace action
{

namespace builder
{

class Init_Drone_Result_final_pos
{
public:
  Init_Drone_Result_final_pos()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::drone_interfaces::action::Drone_Result final_pos(::drone_interfaces::action::Drone_Result::_final_pos_type arg)
  {
    msg_.final_pos = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::action::Drone_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::action::Drone_Result>()
{
  return drone_interfaces::action::builder::Init_Drone_Result_final_pos();
}

}  // namespace drone_interfaces


namespace drone_interfaces
{

namespace action
{

namespace builder
{

class Init_Drone_Feedback_current_pos
{
public:
  Init_Drone_Feedback_current_pos()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::drone_interfaces::action::Drone_Feedback current_pos(::drone_interfaces::action::Drone_Feedback::_current_pos_type arg)
  {
    msg_.current_pos = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::action::Drone_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::action::Drone_Feedback>()
{
  return drone_interfaces::action::builder::Init_Drone_Feedback_current_pos();
}

}  // namespace drone_interfaces


namespace drone_interfaces
{

namespace action
{

namespace builder
{

class Init_Drone_SendGoal_Request_goal
{
public:
  explicit Init_Drone_SendGoal_Request_goal(::drone_interfaces::action::Drone_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::drone_interfaces::action::Drone_SendGoal_Request goal(::drone_interfaces::action::Drone_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::action::Drone_SendGoal_Request msg_;
};

class Init_Drone_SendGoal_Request_goal_id
{
public:
  Init_Drone_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Drone_SendGoal_Request_goal goal_id(::drone_interfaces::action::Drone_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Drone_SendGoal_Request_goal(msg_);
  }

private:
  ::drone_interfaces::action::Drone_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::action::Drone_SendGoal_Request>()
{
  return drone_interfaces::action::builder::Init_Drone_SendGoal_Request_goal_id();
}

}  // namespace drone_interfaces


namespace drone_interfaces
{

namespace action
{

namespace builder
{

class Init_Drone_SendGoal_Response_stamp
{
public:
  explicit Init_Drone_SendGoal_Response_stamp(::drone_interfaces::action::Drone_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::drone_interfaces::action::Drone_SendGoal_Response stamp(::drone_interfaces::action::Drone_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::action::Drone_SendGoal_Response msg_;
};

class Init_Drone_SendGoal_Response_accepted
{
public:
  Init_Drone_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Drone_SendGoal_Response_stamp accepted(::drone_interfaces::action::Drone_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Drone_SendGoal_Response_stamp(msg_);
  }

private:
  ::drone_interfaces::action::Drone_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::action::Drone_SendGoal_Response>()
{
  return drone_interfaces::action::builder::Init_Drone_SendGoal_Response_accepted();
}

}  // namespace drone_interfaces


namespace drone_interfaces
{

namespace action
{

namespace builder
{

class Init_Drone_GetResult_Request_goal_id
{
public:
  Init_Drone_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::drone_interfaces::action::Drone_GetResult_Request goal_id(::drone_interfaces::action::Drone_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::action::Drone_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::action::Drone_GetResult_Request>()
{
  return drone_interfaces::action::builder::Init_Drone_GetResult_Request_goal_id();
}

}  // namespace drone_interfaces


namespace drone_interfaces
{

namespace action
{

namespace builder
{

class Init_Drone_GetResult_Response_result
{
public:
  explicit Init_Drone_GetResult_Response_result(::drone_interfaces::action::Drone_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::drone_interfaces::action::Drone_GetResult_Response result(::drone_interfaces::action::Drone_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::action::Drone_GetResult_Response msg_;
};

class Init_Drone_GetResult_Response_status
{
public:
  Init_Drone_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Drone_GetResult_Response_result status(::drone_interfaces::action::Drone_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Drone_GetResult_Response_result(msg_);
  }

private:
  ::drone_interfaces::action::Drone_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::action::Drone_GetResult_Response>()
{
  return drone_interfaces::action::builder::Init_Drone_GetResult_Response_status();
}

}  // namespace drone_interfaces


namespace drone_interfaces
{

namespace action
{

namespace builder
{

class Init_Drone_FeedbackMessage_feedback
{
public:
  explicit Init_Drone_FeedbackMessage_feedback(::drone_interfaces::action::Drone_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::drone_interfaces::action::Drone_FeedbackMessage feedback(::drone_interfaces::action::Drone_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::action::Drone_FeedbackMessage msg_;
};

class Init_Drone_FeedbackMessage_goal_id
{
public:
  Init_Drone_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Drone_FeedbackMessage_feedback goal_id(::drone_interfaces::action::Drone_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Drone_FeedbackMessage_feedback(msg_);
  }

private:
  ::drone_interfaces::action::Drone_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::action::Drone_FeedbackMessage>()
{
  return drone_interfaces::action::builder::Init_Drone_FeedbackMessage_goal_id();
}

}  // namespace drone_interfaces

#endif  // DRONE_INTERFACES__ACTION__DETAIL__DRONE__BUILDER_HPP_
