export const metadata = { title: "JobMateAI", description: "CV ↔ JD match" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
