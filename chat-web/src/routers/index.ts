import React from "react";
import { createBrowserRouter } from "react-router";
import Home from "@/views/Home";
import Login from "@/views/Login";

const router = createBrowserRouter([
  {
    path: "/",
    element: React.createElement(Login),
  },
  {
    path: "/home",
    element: React.createElement(Home),
  }
]);

export default router;
