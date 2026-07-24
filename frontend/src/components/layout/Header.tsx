function Header() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-white px-6 shadow-sm">
      <h1 className="text-xl font-bold">
        AI Customer Support
      </h1>

      <button
        className="rounded bg-red-600 px-4 py-2 text-white hover:bg-red-700"
      >
        Logout
      </button>
    </header>
  );
}

export default Header;