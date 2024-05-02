import React, { useState } from "react";
import {
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
} from "@ant-design/icons";
import { Layout, Menu, theme } from "antd";
import SendMessageBar from "@/components/SendMessageBar";

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

  // 动态计算content区域的高度
  const [footerHeight, setFooterHeight] = useState<number>(0);
  const handleFooterResize = (height: number) => {
    setFooterHeight(height);
  };
  const viewportHeight = window.innerHeight;
  const contentHeight = viewportHeight - footerHeight - 144;

  const sendMessage = (value: string) => {
    console.log(value);
    // 这里可以添加发送消息的逻辑
  };

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
          <SendMessageBar
            onSendMessage={sendMessage}
            onResize={(e) => handleFooterResize(e.height)}
          />
        </Footer>
      </Layout>
    </Layout>
  );
};

export default Home;
