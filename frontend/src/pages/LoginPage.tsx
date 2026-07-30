import {
  Bot,
  Database,
  MessageSquare,
  ShieldCheck,
} from "lucide-react";

import {
  useState,
} from "react";

import {
  Link,
  useNavigate,
} from "react-router-dom";

import {
  login,
} from "../features/auth/services/authService";


function LoginPage() {
  const navigate = useNavigate();

  const [
    username,
    setUsername,
  ] = useState("");

  const [
    password,
    setPassword,
  ] = useState("");

  const [
    loading,
    setLoading,
  ] = useState(false);


  async function handleLogin() {

    if (!username || !password) {
      alert(
        "Please enter your email and password.",
      );
      return;
    }


    setLoading(true);


    try {

      const response = await login({
        username,
        password,
      });


      localStorage.setItem(
        "access_token",
        response.access_token,
      );


      navigate("/dashboard");


    } catch (error) {

      console.error(error);

      alert(
        "Invalid email or password.",
      );


    } finally {

      setLoading(false);

    }
  }


  return (

    <div
      className="
        min-h-screen
        grid
        lg:grid-cols-2
        bg-slate-950
      "
    >

      {/* LEFT BRAND PANEL */}

      <div
        className="
          hidden
          lg:flex
          flex-col
          justify-between
          p-12
          xl:p-20
          bg-gradient-to-br
          from-blue-700
          via-indigo-700
          to-slate-900
          text-white
        "
      >

        <div>

          <div
            className="
              flex
              items-center
              gap-3
              mb-12
            "
          >

            <div
              className="
                flex
                h-14
                w-14
                items-center
                justify-center
                rounded-2xl
                bg-white/20
                backdrop-blur
              "
            >

              <Bot size={32}/>

            </div>


            <div>

              <h1
                className="
                  text-2xl
                  font-bold
                "
              >
                AI Support
              </h1>


              <p
                className="
                  text-sm
                  text-blue-100
                "
              >
                Customer Intelligence Platform
              </p>

            </div>


          </div>



          <h2
            className="
              text-4xl
              xl:text-5xl
              font-bold
              leading-tight
            "
          >
            Intelligent
            <br/>
            Customer Support
            <br/>
            Powered by AI
          </h2>


          <p
            className="
              mt-6
              max-w-lg
              text-lg
              text-blue-100
            "
          >
            Search company knowledge,
            answer customer questions,
            and automate support using
            Retrieval-Augmented Generation.
          </p>


          <div
            className="
              mt-12
              space-y-5
            "
          >

            <Feature
              icon={<MessageSquare size={20}/>}
              text="AI conversations"
            />

            <Feature
              icon={<Database size={20}/>}
              text="Knowledge base RAG search"
            />

            <Feature
              icon={<ShieldCheck size={20}/>}
              text="Secure user workspace"
            />

          </div>

        </div>


        <p
          className="
            text-sm
            text-blue-200
          "
        >
          © 2026 AI Customer Support Platform
        </p>


      </div>




      {/* LOGIN PANEL */}

      <div
        className="
          flex
          items-center
          justify-center
          px-6
          py-12
          bg-gradient-to-br
          from-slate-100
          to-blue-50
        "
      >

        <div
          className="
            w-full
            max-w-md
            rounded-3xl
            border
            border-white
            bg-white/90
            p-8
            sm:p-10
            shadow-2xl
            backdrop-blur
          "
        >


          {/* MOBILE LOGO */}

          <div
            className="
              mb-8
              text-center
              lg:hidden
            "
          >

            <div
              className="
                mx-auto
                mb-4
                flex
                h-16
                w-16
                items-center
                justify-center
                rounded-2xl
                bg-blue-600
                text-white
              "
            >

              <Bot size={34}/>

            </div>


            <h1
              className="
                text-2xl
                font-bold
              "
            >
              AI Customer Support
            </h1>

          </div>



          <h2
            className="
              text-3xl
              font-bold
              text-slate-900
            "
          >
            Welcome back
          </h2>


          <p
            className="
              mt-2
              text-slate-500
            "
          >
            Sign in to continue to your dashboard.
          </p>




          <div className="mt-8">


            <label
              className="
                mb-2
                block
                text-sm
                font-medium
                text-slate-700
              "
            >
              Email Address
            </label>


            <input
              type="email"
              value={username}
              placeholder="you@example.com"
              onChange={(e)=>
                setUsername(e.target.value)
              }
              className="
                w-full
                rounded-xl
                border
                border-slate-300
                bg-slate-50
                px-4
                py-3
                outline-none
                transition
                focus:border-blue-500
                focus:bg-white
              "
            />

          </div>



          <div className="mt-5">


            <label
              className="
                mb-2
                block
                text-sm
                font-medium
                text-slate-700
              "
            >
              Password
            </label>


            <input
              type="password"
              value={password}
              placeholder="••••••••"
              onChange={(e)=>
                setPassword(e.target.value)
              }
              onKeyDown={(e)=>{
                if(e.key==="Enter"){
                  handleLogin();
                }
              }}
              className="
                w-full
                rounded-xl
                border
                border-slate-300
                bg-slate-50
                px-4
                py-3
                outline-none
                transition
                focus:border-blue-500
                focus:bg-white
              "
            />

          </div>



          <button
            onClick={handleLogin}
            disabled={loading}
            className="
              mt-7
              w-full
              rounded-xl
              bg-blue-600
              py-3
              font-semibold
              text-white
              shadow-lg
              transition
              hover:bg-blue-700
              disabled:bg-slate-400
            "
          >

            {
              loading
              ? "Signing In..."
              : "Sign In"
            }

          </button>



          <p
            className="
              mt-8
              text-center
              text-sm
              text-slate-500
            "
          >

            Don't have an account?{" "}

            <Link
              to="/register"
              className="
                font-semibold
                text-blue-600
              "
            >
              Create one
            </Link>

          </p>


        </div>


      </div>


    </div>

  );
}



function Feature({
  icon,
  text,
}: {
  icon: React.ReactNode;
  text: string;
}) {

  return (

    <div
      className="
        flex
        items-center
        gap-3
        text-blue-100
      "
    >

      <div
        className="
          rounded-lg
          bg-white/10
          p-2
        "
      >
        {icon}
      </div>

      <span>
        {text}
      </span>

    </div>

  );
}


export default LoginPage;