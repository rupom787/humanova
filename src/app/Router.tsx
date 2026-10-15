import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import { AppShell } from '@/components/layouts/AppShell';
import { Login } from '@/pages/auth/Login';
import { Register } from '@/pages/auth/Register';
import { Dashboard } from '@/pages/dashboard/Dashboard';
import { AiStudio } from '@/pages/ai-studio/AiStudio';
import { Verification } from '@/pages/verification/Verification';
import { Analytics } from '@/pages/analytics/Analytics';
import { Community } from '@/pages/community/Community';
import { Reports } from '@/pages/reports/Reports';
import { Settings } from '@/pages/settings/Settings';
import { Home } from '@/pages/Home';
import { GlobalToaster } from '@/components/ui/basic-toast';

export const Router: React.FC = () => {
  const { isAuthenticated } = useAuthStore();

  return (
    <BrowserRouter>
      <GlobalToaster />
      <Routes>
        {/* Public Landing Page */}
        <Route path="/" element={<Home />} />

        {/* Auth Routes */}
        <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" />} />
        <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" />} />

        {/* Protected App Routes */}
        <Route
          path="/*"
          element={
            isAuthenticated ? (
              <AppShell>
                <Routes>
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/ai-studio" element={<AiStudio />} />
                  <Route path="/verification" element={<Verification />} />
                  <Route path="/verification/:scanId" element={<Verification />} />
                  <Route path="/analytics" element={<Analytics />} />
                  <Route path="/community" element={<Community />} />
                  <Route path="/reports" element={<Reports />} />
                  <Route path="/settings" element={<Settings />} />
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </AppShell>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
      </Routes>
    </BrowserRouter>
  );
};
