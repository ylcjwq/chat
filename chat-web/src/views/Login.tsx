import React from "react";
import { Form, Input, Button, Card } from "antd";
import {
  UserOutlined,
  LockOutlined,
  EyeInvisibleOutlined,
  EyeTwoTone,
} from "@ant-design/icons";
import { postLogin } from "@/api/request";
import "@/styles/login.css";
import { useNavigate } from "react-router";

const Login: React.FC = () => {
  const navigate = useNavigate();

  const onFinish = async (values: any) => {
    const res = await postLogin(values);
    const data = await res.json();
    localStorage.setItem("token", data.token);
    // 跳转到聊天页面
    navigate("/home");
  };

  return (
    <div className="login-container">
      <Card title="登录" className="login-card">
        <Form
          name="normal_login"
          className="login-form"
          initialValues={{ remember: true }}
          onFinish={onFinish}
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: "请输入用户名!" }]}
          >
            <Input
              prefix={<UserOutlined className="site-form-item-icon" />}
              placeholder="用户名"
            />
          </Form.Item>
          <Form.Item
            name="password"
            rules={[{ required: true, message: "请输入密码!" }]}
          >
            <Input.Password
              prefix={<LockOutlined className="site-form-item-icon" />}
              type="password"
              placeholder="密码"
              iconRender={(visible) =>
                visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />
              }
            />
          </Form.Item>
          <Form.Item>
            <div className="login-form-button-container">
              <Button
                type="primary"
                htmlType="submit"
                className="login-form-button"
              >
                登录
                <div className="hoverEffect">
                  <div></div>
                </div>
              </Button>
            </div>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default Login;
