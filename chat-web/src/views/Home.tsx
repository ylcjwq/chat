import React, { useState } from "react";
import {
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
} from "@ant-design/icons";
import { Layout, Menu, theme, Input, Button, Space } from "antd";

const { Header, Content, Footer, Sider } = Layout;

const items = [
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  UserOutlined,
].map((icon, index) => ({
  key: String(index + 1),
  icon: React.createElement(icon),
  label: `nav ${index + 1}`,
}));

const Home: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const [footerHeight, setFooterHeight] = useState<number>(0);
  const handleFooterResize = (height: number) => {
    setFooterHeight(height);
  };
  const contentHeight = `calc(100vh - 64px - ${footerHeight}px -50px)`; // 动态计算内容区域高度

  return (
    <Layout>
      <Sider breakpoint="lg" collapsedWidth="0">
        <div className="demo-logo-vertical" />
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={["4"]}
          items={items}
        />
      </Sider>
      <Layout>
        <Header style={{ padding: 0, background: colorBgContainer }} />
        <Content style={{ margin: "10px 10px 0" }}>
          <div
            style={{
              padding: 20,
              height: contentHeight,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            content
          </div>
        </Content>
        <Footer style={{ textAlign: "center" }}>
          <Space.Compact style={{ width: "100%" }}>
            <Input.TextArea
              allowClear
              maxLength={2000}
              showCount
              autoSize={{ minRows: 1, maxRows: 3 }}
              onResize={(e) => handleFooterResize(e.height)}
              placeholder="请输入"
            />
          </Space.Compact>
        </Footer>
      </Layout>
    </Layout>
  );
};

export default Home;
