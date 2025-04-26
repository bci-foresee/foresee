/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production';

const nextConfig = {
  // Generate static HTML files in "out" dir to be loaded by Electron in production
  output: "export",

  // No assetPrefix needed. Electron will run a tiny local HTTP server in
  // production so absolute "_next/static/*" URLs resolve correctly.

  images: { unoptimized: true },     // needed for static export
};

export default nextConfig;
