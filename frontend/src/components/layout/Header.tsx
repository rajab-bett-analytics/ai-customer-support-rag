function Header() {
  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b bg-white px-8 shadow-sm">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">
          AI Customer Support
        </h1>

        <p className="text-sm text-gray-500">
          Intelligent Customer Support Platform
        </p>
      </div>

      <button
        className="flex items-center gap-2 rounded-lg border border-red-500 px-4 py-2 text-sm font-medium text-red-600 transition duration-200 hover:bg-red-600 hover:text-white"
      >
        <span>🚪</span>
        Logout
      </button>
    </header>
  );
}

export default Header;