import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'AsterDEX Cosmic Trader',
  description: 'Trading on vibes and astrology',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
