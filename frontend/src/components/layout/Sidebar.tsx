import NavigationItem from "./NavigationItem";

function Sidebar() {
  return (
    <aside className="flex h-full w-72 flex-col border-r bg-white p-4">
      <nav className="space-y-2">
        <NavigationItem
          to="/dashboard"
          label="💬 Chat"
        />

        <NavigationItem
          to="/documents"
          label="📄 Documents"
        />

        <NavigationItem
          to="/analytics"
          label="📊 Analytics"
        />

        <NavigationItem
          to="/profile"
          label="👤 Profile"
        />
      </nav>
    </aside>
  );
}

export default Sidebar;