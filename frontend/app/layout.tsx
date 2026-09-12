import "./globals.css";

export const metadata = {
  title: "Doc Intelligence Platform",
  description: "AI-powered document querying and analytics",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
