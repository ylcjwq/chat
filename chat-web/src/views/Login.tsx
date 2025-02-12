import React from "react";
import { Form, Input, Button, Card } from "antd";
import {
  UserOutlined,
  LockOutlined,
  EyeInvisibleOutlined,
  EyeTwoTone,
} from "@ant-design/icons";
import "@/styles/login.css";

const Login: React.FC = () => {
  const onFinish = (values: any) => {
    console.log("Received values of form: ", values);
    // 在这里处理登录逻辑
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
