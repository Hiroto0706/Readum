import React from "react";
import Image from "next/image";
import Link from "next/link";

export const Header: React.FC = () => {
  return (
    <header className="bg-emerald-500 h-16 w-full flex items-center justify-between px-2 md:px-8 absolute top-0 left-0">
      <div className="flex items-center">
        <Image src="/icons/icon.svg" alt="Readum logo" width={40} height={40} />
        <span className="text-white text-xl font-bold ml-2">Readum</span>
      </div>

      <Link
        href="/about"
        className="flex items-center text-white font-bold py-2 px-4 rounded-full hover:bg-white/30 transition-all duration-300"
      >
        <Image
          src="/icons/generate.svg"
          alt="Generate icon"
          width={20}
          height={20}
          className="mr-2"
        />
        <span>about</span>
      </Link>
    </header>
  );
};
