import { NavLink } from "react-router-dom";

interface NavigationItemProps {
  to: string;
  label: string;
}

function NavigationItem({
  to,
  label,
}: NavigationItemProps) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `block rounded-lg px-4 py-3 transition ${
          isActive
            ? "bg-blue-600 text-white"
            : "text-gray-700 hover:bg-gray-100"
        }`
      }
    >
      {label}
    </NavLink>
  );
}

export default NavigationItem;