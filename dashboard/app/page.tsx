'use client'

import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface Stats {
  timestamp: string
  balance: {
    eth: number
    usd: number
    eth_price: number
  }
  positions: Array<{
    symbol: string
    side: string
    quantity: number
    entryPrice: number
    markPrice: number
    pnl: number
    pnlPercent: number
  }>
  totalPnL: number
  openPositions: number
  leverageRange: string
}

interface HistoryPoint {
  timestamp: string
  balanceUsd: number
  totalPnL: number
  openPositions: number
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [history, setHistory] = useState<HistoryPoint[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, historyRes] = await Promise.all([
          fetch('/stats.json?t=' + Date.now()), // Cache busting
          fetch('/history.json?t=' + Date.now())
        ])

        if (!statsRes.ok || !historyRes.ok) {
          throw new Error('Failed to fetch data')
        }

        const statsData = await statsRes.json()
        const historyData = await historyRes.json()

        setStats(statsData)
        setHistory(historyData)
        setLoading(false)
      } catch (error) {
        console.error('Error fetching data:', error)
        setLoading(false) // Stop loading even on error
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 30000) // Refresh every 30 seconds

    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🌙</div>
          <div className="text-xl">Loading cosmic data...</div>
        </div>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">⚠️</div>
          <div className="text-xl mb-4">No cosmic data available</div>
          <div className="text-sm text-gray-400">
            Run the trading bot to generate stats:<br/>
            <code className="bg-gray-800 px-2 py-1 rounded mt-2 inline-block">
              python autonomous_cosmic_trader.py
            </code>
          </div>
        </div>
      </div>
    )
  }

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold mb-2">🌙 ✨ Cosmic Trader Dashboard ✨ 🌙</h1>
          <p className="text-xl text-gray-300">Trading on pure vibes and astrology</p>
          <p className="text-sm text-gray-400 mt-2">
            Last updated: {new Date(stats.timestamp).toLocaleString()}
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Balance */}
          <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 rounded-lg p-6 border border-purple-500/30">
            <div className="text-gray-300 mb-2">💰 Balance</div>
            <div className="text-3xl font-bold">${stats.balance.usd.toFixed(2)}</div>
            <div className="text-sm text-gray-400 mt-1">
              {stats.balance.eth.toFixed(4)} ETH
            </div>
          </div>

          {/* Total PnL */}
          <div className={`rounded-lg p-6 border ${
            stats.totalPnL >= 0
              ? 'bg-gradient-to-br from-green-900/50 to-emerald-900/50 border-green-500/30'
              : 'bg-gradient-to-br from-red-900/50 to-rose-900/50 border-red-500/30'
          }`}>
            <div className="text-gray-300 mb-2">📊 Total PnL</div>
            <div className="text-3xl font-bold">
              {stats.totalPnL >= 0 ? '+' : ''}${stats.totalPnL.toFixed(2)}
            </div>
            <div className="text-sm text-gray-400 mt-1">
              {stats.totalPnL >= 0 ? '🚀 To the moon!' : '📉 Cosmos giveth and taketh'}
            </div>
          </div>

          {/* Open Positions */}
          <div className="bg-gradient-to-br from-indigo-900/50 to-purple-900/50 rounded-lg p-6 border border-indigo-500/30">
            <div className="text-gray-300 mb-2">🎯 Open Positions</div>
            <div className="text-3xl font-bold">{stats.openPositions}</div>
            <div className="text-sm text-gray-400 mt-1">
              {stats.leverageRange} Leverage (cosmos decides!)
            </div>
          </div>
        </div>

        {/* Chart */}
        {history.length > 0 && (
          <div className="bg-gray-900/50 rounded-lg p-6 mb-8 border border-gray-700/50">
            <h2 className="text-2xl font-bold mb-4">📈 Balance History (24h)</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis
                  dataKey="timestamp"
                  tickFormatter={formatTime}
                  stroke="#9CA3AF"
                />
                <YAxis stroke="#9CA3AF" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                  formatter={(value: number) => `$${value.toFixed(2)}`}
                  labelFormatter={(label: string) => new Date(label).toLocaleString()}
                />
                <Line
                  type="monotone"
                  dataKey="balanceUsd"
                  stroke="#8B5CF6"
                  strokeWidth={2}
                  dot={false}
                  name="Balance"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Positions */}
        {stats.positions.length > 0 && (
          <div className="bg-gray-900/50 rounded-lg p-6 border border-gray-700/50">
            <h2 className="text-2xl font-bold mb-4">🔮 Current Positions</h2>
            <div className="space-y-4">
              {stats.positions.map((position: {
                symbol: string;
                side: string;
                quantity: number;
                entryPrice: number;
                markPrice: number;
                pnl: number;
                pnlPercent: number;
              }, index: number) => (
                <div
                  key={index}
                  className={`p-4 rounded-lg border ${
                    position.pnl >= 0
                      ? 'bg-green-900/20 border-green-500/30'
                      : 'bg-red-900/20 border-red-500/30'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="text-xl font-bold">{position.symbol}</div>
                      <div className={`inline-block px-2 py-1 rounded text-sm mt-1 ${
                        position.side === 'LONG'
                          ? 'bg-green-500/20 text-green-300'
                          : 'bg-red-500/20 text-red-300'
                      }`}>
                        {position.side}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={`text-2xl font-bold ${
                        position.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {position.pnl >= 0 ? '+' : ''}${position.pnl.toFixed(2)}
                      </div>
                      <div className="text-sm text-gray-400">
                        {position.pnlPercent >= 0 ? '+' : ''}{position.pnlPercent.toFixed(2)}%
                      </div>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-4 mt-3 text-sm">
                    <div>
                      <div className="text-gray-400">Entry</div>
                      <div className="font-mono">${position.entryPrice.toFixed(4)}</div>
                    </div>
                    <div>
                      <div className="text-gray-400">Current</div>
                      <div className="font-mono">${position.markPrice.toFixed(4)}</div>
                    </div>
                    <div>
                      <div className="text-gray-400">Quantity</div>
                      <div className="font-mono">{position.quantity.toFixed(4)}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {stats.positions.length === 0 && (
          <div className="bg-gray-900/50 rounded-lg p-12 text-center border border-gray-700/50">
            <div className="text-6xl mb-4">🌙</div>
            <div className="text-xl text-gray-400">
              No open positions - waiting for cosmic signals...
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
