import NavigationItem from "./NavigationItem";
import { sidebarNavigation } from "./navigation";

export default function SidebarNavigation() {
  return (
    <nav
      className="
        flex
        flex-1
        flex-col
        px-3
        py-4
      "
    >
      <div className="space-y-2">
        {sidebarNavigation.map((item) => (
          <NavigationItem
            key={item.path}
            {...item}
          />
        ))}
      </div>
    </nav>
  );
}