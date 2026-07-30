import {
  createContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";

interface LayoutContextType {
  // Sidebar
  sidebarCollapsed: boolean;
  setSidebarCollapsed: (
    value: boolean,
  ) => void;

  mobileSidebarOpen: boolean;
  setMobileSidebarOpen: (
    value: boolean,
  ) => void;

  // Document Preview
  previewVisible: boolean;
  setPreviewVisible: (
    value: boolean,
  ) => void;

  // Panel Sizes
  conversationWidth: number;
  setConversationWidth: (
    value: number,
  ) => void;

  previewWidth: number;
  setPreviewWidth: (
    value: number,
  ) => void;
}

const LayoutContext =
  createContext<LayoutContextType | null>(null);


interface LayoutProviderProps {
  children: ReactNode;
}


const DEFAULT_CONVERSATION_WIDTH = 320;

const DEFAULT_PREVIEW_WIDTH = 420;


export function LayoutProvider({
  children,
}: LayoutProviderProps) {

  const [
    sidebarCollapsed,
    setSidebarCollapsed,
  ] = useState(false);


  const [
    mobileSidebarOpen,
    setMobileSidebarOpen,
  ] = useState(false);


  const [
    previewVisible,
    setPreviewVisible,
  ] = useState(false);


  const [
    conversationWidth,
    setConversationWidth,
  ] = useState(
    DEFAULT_CONVERSATION_WIDTH,
  );


  const [
    previewWidth,
    setPreviewWidth,
  ] = useState(
    DEFAULT_PREVIEW_WIDTH,
  );


  const value = useMemo(
    () => ({
      sidebarCollapsed,
      setSidebarCollapsed,

      mobileSidebarOpen,
      setMobileSidebarOpen,

      previewVisible,
      setPreviewVisible,

      conversationWidth,
      setConversationWidth,

      previewWidth,
      setPreviewWidth,
    }),
    [
      sidebarCollapsed,
      mobileSidebarOpen,
      previewVisible,
      conversationWidth,
      previewWidth,
    ],
  );


  return (
    <LayoutContext.Provider
      value={value}
    >
      {children}
    </LayoutContext.Provider>
  );
}


export { LayoutContext };