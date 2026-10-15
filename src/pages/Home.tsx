import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ShieldAlert,
  ArrowRight,
  ExternalLink,
  Cpu,
  Clock,
  Sparkles,
  Shield,
  FileCheck,
  Zap,
  MousePointerClick
} from 'lucide-react';
import { useAuthStore } from '@/stores/authStore';
import { useUiStore } from '@/stores/uiStore';
import { Terminal, CheckCircle2, AlertTriangle, Activity, RefreshCw, FileText } from 'lucide-react';
import { TextRotate } from '@/components/ui/text-rotate';
import Floating, { FloatingElement } from '@/components/ui/parallax-floating';
import { Button as RainbowButton } from '@/components/ui/rainbow-borders-button';
import { LetterSwapForward } from '@/components/ui/letter-swap';
import SkewCards from '@/components/ui/gradient-card-showcase';
import FlowArt, { FlowSection } from '@/components/ui/story-scroll';
import { renderCanvas } from '@/components/ui/canvas';
import { Component as HorizonHeroSection } from '@/components/ui/horizon-hero-section';
import { CipherHeadline } from '@/components/ui/cipher-headline';
import { ConsensusMap } from '@/components/shared/consensus-map';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';

gsap.registerPlugin(ScrollTrigger);

// Custom CountUp hook for premium analytical feel
const CountUp: React.FC<{ end: number; duration?: number; suffix?: string }> = ({ end, duration = 1.5, suffix = '' }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let start = 0;
    const increment = end / (duration * 60);
    const handle = setInterval(() => {
      start += increment;
      if (start >= end) {
        setCount(end);
        clearInterval(handle);
      } else {
        setCount(Math.floor(start * 10) / 10);
      }
    }, 1000 / 60);

    return () => clearInterval(handle);
  }, [end, duration]);

  return <span className="font-display font-bold">{count.toLocaleString()}{suffix}</span>;
};

// Mouse-tracking card glow component (classic Aceternity / 21st.dev effect)
const GlowCard: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => {
  const cardRef = useRef<HTMLDivElement | null>(null);
  const [coords, setCoords] = useState({ x: 0, y: 0 });
  const [hovered, setHovered] = useState(false);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    setCoords({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    });
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className={`group relative rounded-xl border border-border-subtle bg-surface/40 hover:bg-surface/60 transition-all duration-300 overflow-hidden ${className}`}
    >
      {/* Radial Hover glow border */}
      {hovered && (
        <div
          className="absolute pointer-events-none w-48 h-48 rounded-full blur-[32px] opacity-25 mix-blend-screen transition-opacity duration-300"
          style={{
            background: 'radial-gradient(circle, var(--accent-primary) 0%, transparent 80%)',
            left: coords.x - 96,
            top: coords.y - 96,
          }}
        />
      )}
      <div className="relative z-10">{children}</div>
    </div>
  );
};

// Premium Unsplash images matching the dark cyan high-tech trust governance aesthetic of Humanova
const exampleImages = [
  {
    url: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600&auto=format&fit=crop",
    title: "Abstract Technological Glass",
  },
  {
    url: "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=600&auto=format&fit=crop",
    title: "Cyan Neon Fiber Mesh Network",
  },
  {
    url: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=600&auto=format&fit=crop",
    title: "Matrix Coding Flow",
  },
  {
    url: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=600&auto=format&fit=crop",
    title: "AI Security Shield Representation",
  },
  {
    url: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=600&auto=format&fit=crop",
    title: "Advanced Data Visualization UI Dashboard Detail",
  },
];

// Concentric animated orbital radar widget for idle status preview
const OrbitalRadar: React.FC = () => {
  return (
    <div className="relative w-28 h-28 mx-auto flex items-center justify-center pointer-events-none my-1">
      {/* Outer spinning dash ring */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 15, repeat: Infinity, ease: 'linear' }}
        className="absolute inset-0 rounded-full border border-dashed border-accent-primary/20"
      />
      {/* Inner reverse spinning dash ring */}
      <motion.div
        animate={{ rotate: -360 }}
        transition={{ duration: 10, repeat: Infinity, ease: 'linear' }}
        className="absolute inset-2 rounded-full border border-dotted border-border"
      />
      {/* Concentric solid rings */}
      <div className="absolute inset-5 rounded-full border border-accent-primary/10 flex items-center justify-center">
        <div className="w-14 h-14 rounded-full border border-border flex items-center justify-center">
          <div className="w-8 h-8 rounded-full bg-accent-glow/5 border border-accent-primary/30 flex items-center justify-center">
            <Activity className="w-4 h-4 text-accent-primary animate-pulse" />
          </div>
        </div>
      </div>
      {/* Sweeping radar beam */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
        className="absolute inset-0 rounded-full bg-gradient-to-r from-accent-primary/5 via-transparent to-transparent"
        style={{ transformOrigin: 'center' }}
      />
    </div>
  );
};

// Real-time terminal log typewriter simulator during ingest analysis
const allLogs = [
  '● INGEST: Reading target statement stream...',
  '● NLP: Parsing claims, entities, and assertions... OK',
  '● REGISTRY: Querying verifier consensus nodes... OK',
  '● PARSER: Graphing citation path networks... OK',
  '● CONSENSUS: Calibrating verifier consensus score...',
];

const AuditingConsole: React.FC = () => {
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    const timers: number[] = [];
    allLogs.forEach((log, idx) => {
      const timer = window.setTimeout(() => {
        setLogs(prev => [...prev, log]);
      }, idx * 400);
      timers.push(timer);
    });
    return () => timers.forEach(window.clearTimeout);
  }, []);

  return (
    <div className="font-mono text-[9px] text-[#A7F3D0]/80 space-y-1 h-[100px] text-left">
      {logs.map((log, idx) => (
        <div key={idx} className="flex items-start gap-1">
          <span className="text-accent-primary shrink-0">&gt;</span>
          <span>{log}</span>
        </div>
      ))}
      {logs.length < allLogs.length && (
        <div className="w-1.5 h-3 bg-[#A7F3D0] inline-block animate-pulse ml-1" />
      )}
    </div>
  );
};

export const Home: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const { addNotification } = useUiStore();

  const handleDownloadCertificate = () => {
    addNotification('Trust SLA Compliance Certificate generated and downloaded successfully.', 'success');
  };

  // Trust Sandbox demo states
  const [sandboxPrompt, setSandboxPrompt] = useState('Nvidia Blackwell is officially certified as carbon-neutral by the World Carbon Council.');
  const [isAuditing, setIsAuditing] = useState(false);
  const [auditComplete, setAuditComplete] = useState(false);

  // Instantiate Lenis smooth inertia scrolling
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.4, // Ultra-smooth inertia
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // standard exponential ease
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1.0,
      touchMultiplier: 1.5,
    });

    // Synchronize Lenis scrolling updates with GSAP ScrollTriggers
    lenis.on('scroll', ScrollTrigger.update);

    const updatePhysics = (time: number) => {
      lenis.raf(time * 1000);
    };

    gsap.ticker.add(updatePhysics);

    return () => {
      lenis.destroy();
      gsap.ticker.remove(updatePhysics);
    };
  }, []);

  const handleSandboxVerify = () => {
    if (isAuditing) return;
    setIsAuditing(true);
    setAuditComplete(false);
    useUiStore.getState().setSandboxAuditing(true);

    setTimeout(() => {
      setIsAuditing(false);
      setAuditComplete(true);
      useUiStore.getState().setSandboxAuditing(false);
    }, 2200);
  };

  const handleLaunchConsole = () => {
    if (isAuthenticated) {
      navigate('/dashboard');
    } else {
      navigate('/login');
    }
  };

  const handleSignOut = () => {
    useAuthStore.getState().logout();
    window.location.reload();
  };

  return (
    <div className="relative min-h-[100dvh] bg-bg-primary text-text-primary selection:bg-accent-glow selection:text-accent-primary font-sans overflow-x-hidden scroll-smooth pb-12">
      {/* Tactical procedural newsprint noise grain */}
      <div className="editorial-grain" />

      {/* Springy flowing interactive strand line canvas backdrop */}
      <canvas id="canvas" className="fixed inset-0 w-screen h-screen pointer-events-none z-0" />

      {/* Radial glow background spotlight */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-accent-primary/10 rounded-full blur-[140px] pointer-events-none z-0" />

      {/* Top Navbar Header */}
      <header className="absolute top-0 left-0 right-0 z-20 w-full px-8 h-20 flex items-center justify-between border-b border-white/10 bg-transparent">
        <div className="flex items-center gap-2.5 cursor-pointer group">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-accent-primary to-accent-primary/80 flex items-center justify-center shadow-lg shadow-accent-glow group-hover:brightness-110 transition-all">
            <span className="text-[#FAF8F5] font-display font-black text-sm">H</span>
          </div>
          <LetterSwapForward
            label="Humanova"
            reverse={true}
            staggerFrom="first"
            staggerDuration={0.02}
            className="font-display font-bold text-base tracking-wider bg-gradient-to-r from-accent-primary to-[#FAF8F5] bg-clip-text text-transparent uppercase group-hover:brightness-110"
          />
        </div>

        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <RainbowButton
                onClick={() => navigate('/dashboard')}
                className="h-9 px-4.5 min-w-[120px] rounded-lg text-xs font-display font-black uppercase tracking-wider transition-all cursor-pointer shadow-lg"
              >
                Dashboard
              </RainbowButton>
              <button
                onClick={handleSignOut}
                className="text-xs font-display font-bold uppercase tracking-wider text-[#FAF8F5]/80 hover:text-[#FAF8F5] transition-all cursor-pointer ml-2"
              >
                Sign Out
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => navigate('/login')}
                className="text-xs font-display font-bold uppercase tracking-wider text-[#FAF8F5]/80 hover:text-[#FAF8F5] transition-all cursor-pointer mr-2"
              >
                Sign In
              </button>
              <RainbowButton
                onClick={() => navigate('/register')}
                className="h-9 px-4.5 min-w-[120px] rounded-lg text-xs font-display font-black uppercase tracking-wider transition-all cursor-pointer shadow-lg"
              >
                Create Account
              </RainbowButton>
            </>
          )}
        </div>
      </header>

      {/* 3D WEBGL COSMOS HORIZON HERO SECTION */}
      <HorizonHeroSection />

      {/* IMMERSIVE STORY-SCROLL SECTION */}
      <FlowArt aria-label="Humanova Trust Journey" className="relative z-10">
        <FlowSection aria-label="The Hallucination Crisis" style={{ backgroundColor: '#FFFFFF', color: '#111111' }} className="border-y border-border">
          <p className="text-xs font-display font-bold uppercase tracking-[0.2em] text-accent-primary">01 — The Crisis: Hallucination Risk</p>
          <hr className="my-[2vw] border-none border-t border-border" />
          <div>
            <h1 className="text-[clamp(2.5rem,8vw,9rem)] font-display font-black leading-[0.9] uppercase tracking-tight text-text-primary flex flex-col">
              <CipherHeadline text="HEAR" />
              <CipherHeadline text="EVERYTHING" />
              <CipherHeadline text="TRUST" />
              <CipherHeadline text="NOTHING" />
            </h1>
          </div>
          <hr className="my-[2vw] border-none border-t border-border" />
          <p className="mt-auto max-w-[60ch] text-[clamp(0.95rem,2vw,1.4rem)] font-sans font-medium text-text-secondary leading-relaxed">
            Large language models generate outputs at staggering volumes. Without active verification, enterprise artificial intelligence remains a high-liability, unpredictable black box.
          </p>
        </FlowSection>

        <FlowSection aria-label="The Solution: The Trust Engine" style={{ backgroundColor: '#113524', color: '#FAF8F5' }} className="border-y border-border">
          <p className="text-xs font-display font-bold uppercase tracking-[0.2em] text-[#A7F3D0] opacity-90">02 — The Solution: The Trust Engine</p>
          <hr className="my-[2vw] border-none border-t border-[#FAF8F5]/20" />
          <div>
            <h2 className="text-[clamp(2.5rem,8vw,9rem)] font-display font-black leading-[0.9] uppercase tracking-tight text-[#FAF8F5] flex flex-col">
              <CipherHeadline text="GOVERN" />
              <CipherHeadline text="YOUR" />
              <CipherHeadline text="OUTPUTS" />
            </h2>
          </div>
          <hr className="my-[2vw] border-none border-t border-[#FAF8F5]/20" />
          <p className="max-w-[60ch] text-[clamp(0.95rem,2vw,1.4rem)] font-sans font-medium text-[#FAF8F5]/90 leading-relaxed mb-6">
            Humanova intercept-checks prompt pipelines to scrub hallucinations, audit references, score semantic alignments, and block out critical security vulnerabilities automatically.
          </p>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center w-full mt-4">
            <div className="flex flex-wrap gap-[3vw]">
              <div className="min-w-[180px] flex-1">
                <p className="mb-2 text-xs font-display font-bold uppercase tracking-wider text-[#A7F3D0]">Auditing</p>
                <p className="text-xs text-[#FAF8F5]/80 leading-relaxed">
                  Automatic real-time factuality checks and claim classifications powered by custom verifier consensus.
                </p>
              </div>
              <div className="min-w-[180px] flex-1">
                <p className="mb-2 text-xs font-display font-bold uppercase tracking-wider text-[#A7F3D0]">Citations</p>
                <p className="text-xs text-[#FAF8F5]/80 leading-relaxed">
                  Graphing reference citation networks and verifying live URL link structures for source accuracy.
                </p>
              </div>
              <div className="min-w-[180px] flex-1">
                <p className="mb-2 text-xs font-display font-bold uppercase tracking-wider text-[#A7F3D0]">Safety</p>
                <p className="text-xs text-[#FAF8F5]/80 leading-relaxed">
                  Applying custom moderation filters and semantic alignment guardrails to safeguard organizational assets.
                </p>
              </div>
            </div>
            <div className="w-full flex justify-center lg:justify-end">
              <ConsensusMap />
            </div>
          </div>
        </FlowSection>

        <FlowSection aria-label="The Methodology: Scan. Prove. Deploy." style={{ backgroundColor: '#C85A17', color: '#FAF8F5' }} className="border-y border-border">
          <p className="text-xs font-display font-bold uppercase tracking-[0.2em] text-[#FFF7ED] opacity-90">03 — The Methodology: Scan. Prove. Deploy.</p>
          <hr className="my-[2vw] border-none border-t border-[#FAF8F5]/25" />
          <div>
            <h2 className="text-[clamp(2.5rem,8vw,9rem)] font-display font-black leading-[0.9] uppercase tracking-tight text-[#FAF8F5] flex flex-col">
              <CipherHeadline text="SCAN." />
              <CipherHeadline text="PROVE." />
              <CipherHeadline text="DEPLOY." />
            </h2>
          </div>
          <hr className="my-[2vw] border-none border-t border-[#FAF8F5]/25" />
          <p className="max-w-[60ch] text-[clamp(0.95rem,2vw,1.4rem)] font-sans font-medium text-[#FAF8F5]/90 leading-relaxed mb-6">
            Humanova's precise trust scrubber fits neatly into mission-critical pipelines, checking generative responses in milliseconds.
          </p>
          <div className="flex flex-wrap gap-[3vw]">
            <div className="min-w-[180px] flex-1">
              <p className="mb-2 text-xs font-display font-bold uppercase tracking-wider text-[#FFEDD5]">01 — Intercept</p>
              <p className="text-xs text-[#FAF8F5]/80 leading-relaxed font-medium">
                Tap into your LLM telemetry streams instantly via micro-latency API proxies.
              </p>
            </div>
            <div className="min-w-[180px] flex-1">
              <p className="mb-2 text-xs font-display font-bold uppercase tracking-wider text-[#FFEDD5]">02 — Verify</p>
              <p className="text-xs text-[#FAF8F5]/80 leading-relaxed font-medium">
                Cross-reference assertions against verifiable citation networks and internal knowledge bases.
              </p>
            </div>
            <div className="min-w-[180px] flex-1">
              <p className="mb-2 text-xs font-display font-bold uppercase tracking-wider text-[#FFEDD5]">03 — Enforce</p>
              <p className="text-xs text-[#FAF8F5]/80 leading-relaxed font-medium">
                Apply real-time moderation gates, score responses, and dispatch clean outputs.
              </p>
            </div>
          </div>
        </FlowSection>

        {/* HIGH OCTANE BOLD CRIMSON CONTRAST PANEL */}
        <FlowSection aria-label="Scale: Trusted Enterprise Metrics" style={{ backgroundColor: '#EA1C24', color: '#FAF8F5' }} className="border-y border-border">
          <p className="text-xs font-display font-bold uppercase tracking-[0.2em] text-[#FAF8F5] opacity-90">04 — Scale: Trusted Enterprise Metrics</p>
          <hr className="my-[2vw] border-none border-t border-[#FAF8F5]/30" />
          <div>
            <h2 className="text-[clamp(2.5rem,8vw,9rem)] font-display font-black leading-[0.9] uppercase tracking-tight text-[#FAF8F5] flex flex-col">
              <CipherHeadline text="GOVERNANCE" />
              <CipherHeadline text="BY" />
              <CipherHeadline text="NUMBERS" />
            </h2>
          </div>
          <hr className="my-[2vw] border-none border-t border-[#FAF8F5]/30" />
          <p className="max-w-[60ch] text-[clamp(0.95rem,2vw,1.4rem)] font-sans font-medium text-[#FAF8F5]/90 leading-relaxed mb-6">
            Trusted by security administrators, leading risk verifiers, and third-party auditors globally.
          </p>
          <div className="flex flex-wrap gap-[3vw]">
            <div className="min-w-[180px] flex-1">
              <p className="text-3xl sm:text-4xl font-display font-black text-[#FAF8F5] mb-1">99.8%</p>
              <p className="text-xs text-[#FAF8F5]/75 uppercase font-display font-bold tracking-wider mb-2">Accuracy Index</p>
              <p className="text-xs text-[#FAF8F5]/85 leading-relaxed">
                Hallucination and classification precision verified across thousands of model test-beds.
              </p>
            </div>
            <div className="min-w-[180px] flex-1">
              <p className="text-3xl sm:text-4xl font-display font-black text-[#FAF8F5] mb-1">12ms</p>
              <p className="text-xs text-[#FAF8F5]/75 uppercase font-display font-bold tracking-wider mb-2">Micro-Latency</p>
              <p className="text-xs text-[#FAF8F5]/85 leading-relaxed">
                Average processing overhead latency, guaranteeing instantaneous fact-checking.
              </p>
            </div>
            <div className="min-w-[180px] flex-1">
              <p className="text-3xl sm:text-4xl font-display font-black text-[#FAF8F5] mb-1">Zero</p>
              <p className="text-xs text-[#FAF8F5]/75 uppercase font-display font-bold tracking-wider mb-2">Hallucination Leakage</p>
              <p className="text-xs text-[#FAF8F5]/85 leading-relaxed">
                No unmoderated vulnerabilities are allowed to pass through target verification gateways.
              </p>
            </div>
          </div>
        </FlowSection>

        <FlowSection aria-label="Launch Console" style={{ backgroundColor: '#FFF7C5', color: '#111111' }} className="border-t border-border">
          <p className="text-xs font-display font-bold uppercase tracking-[0.2em] text-accent-primary">05 — Get Started</p>
          <hr className="my-[2vw] border-none border-t border-border" />
          <div>
            <h2 className="text-[clamp(2.5rem,8vw,9rem)] font-display font-black leading-[0.9] uppercase tracking-tight text-text-primary flex flex-col">
              <CipherHeadline text="SECURE" />
              <CipherHeadline text="YOUR" />
              <CipherHeadline text="SYSTEMS" />
            </h2>
          </div>
          <hr className="my-[2vw] border-none border-t border-border" />
          <p className="max-w-[60ch] text-[clamp(0.95rem,2vw,1.4rem)] font-sans font-medium text-text-secondary leading-relaxed mb-8">
            Take command of your organization's generative trust lifecycle. Build verifiable, secure, and compliant AI solutions in minutes.
          </p>
          <div className="flex flex-wrap gap-4 mt-auto">
            {isAuthenticated ? (
              <button
                onClick={() => navigate('/dashboard')}
                className="py-4 px-8 rounded-full bg-gradient-to-r from-accent-secondary to-accent-primary hover:brightness-110 text-bg-primary text-sm font-semibold uppercase tracking-wider shadow-lg shadow-accent-glow flex items-center justify-center gap-2 cursor-pointer transition-all active:scale-98"
              >
                Access Dashboard
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <>
                <button
                  onClick={() => navigate('/register')}
                  className="py-4 px-8 rounded-full bg-gradient-to-r from-accent-secondary to-accent-primary hover:brightness-110 text-bg-primary text-sm font-semibold uppercase tracking-wider shadow-lg shadow-accent-glow flex items-center justify-center gap-2 cursor-pointer transition-all active:scale-98"
                >
                  Create Free Account
                  <ArrowRight className="w-4 h-4" />
                </button>
                <button
                  onClick={() => navigate('/login')}
                  className="py-4 px-8 rounded-full bg-surface/50 hover:bg-surface border border-border text-sm font-semibold uppercase tracking-wider text-text-primary cursor-pointer transition-all active:scale-98 flex items-center justify-center gap-2"
                >
                  Sign In
                </button>
              </>
            )}
          </div>
        </FlowSection>
      </FlowArt>

      {/* Main Container */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 pt-12 md:pt-16 space-y-28">

        {/* INTERACTIVE TRUST SANDBOX DEMO */}
        <section id="demo" className="glass-card p-6 md:p-8 rounded-xl border border-border-subtle relative overflow-hidden space-y-6">
          {/* Top visual accent */}
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-accent-primary to-accent-secondary" />

          <div>
            <span className="text-[10px] font-display font-bold uppercase tracking-wider text-accent-primary">Interactive Scrubber Sandbox</span>
            <h2 className="text-xl md:text-2xl font-display font-bold uppercase text-text-primary mt-1">
              Scrutinize Claims in Real-Time
            </h2>
            <p className="text-xs text-text-secondary mt-0.5 max-w-xl">
              Type or select a factual statement and click "Execute Audit" to witness our alignment parser check references and highlight hallucinations.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">

            {/* Input sandbox console */}
            <div className="flex flex-col justify-between space-y-4">
              <div className="space-y-4">
                {/* Presets */}
                <div className="space-y-2">
                  <label className="text-[9px] font-display font-bold uppercase tracking-wider text-text-muted">Factual Hypotheses Presets</label>
                  <div className="flex flex-col gap-2">
                    <button
                      type="button"
                      onClick={() => {
                        setSandboxPrompt('Nvidia Blackwell is officially certified as carbon-neutral by the World Carbon Council.');
                        setAuditComplete(false);
                      }}
                      className="text-left p-3 rounded-lg bg-surface/30 hover:bg-surface border border-border-subtle/50 text-xs text-text-secondary font-medium transition-all flex items-center justify-between"
                    >
                      <span>"Nvidia Blackwell is officially certified as carbon-neutral by the World Carbon Council."</span>
                      <MousePointerClick className="w-3.5 h-3.5 text-accent-primary opacity-60" />
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setSandboxPrompt('Google Gemini operates under four key safety filters: Hate Speech, Harassment, Sexually Explicit, and Dangerous Content.');
                        setAuditComplete(false);
                      }}
                      className="text-left p-3 rounded-lg bg-surface/30 hover:bg-surface border border-border-subtle/50 text-xs text-text-secondary font-medium transition-all flex items-center justify-between"
                    >
                      <span>"Google Gemini operates under four key safety filters: Hate Speech, Harassment, Sexually Explicit, and Dangerous Content."</span>
                      <MousePointerClick className="w-3.5 h-3.5 text-accent-primary opacity-60" />
                    </button>
                  </div>
                </div>

                {/* Textarea */}
                <div className="space-y-1">
                  <label className="text-[9px] font-display font-bold uppercase tracking-wider text-text-muted">Target Statement</label>
                  <textarea
                    value={sandboxPrompt}
                    onChange={(e) => {
                      setSandboxPrompt(e.target.value);
                      setAuditComplete(false);
                    }}
                    rows={4}
                    className="w-full bg-bg-primary/50 focus:bg-bg-primary border border-border-subtle focus:border-accent-primary focus:outline-none transition-all rounded-lg p-3 text-xs text-text-primary font-medium"
                  />
                </div>
              </div>

              <button
                onClick={handleSandboxVerify}
                disabled={isAuditing || !sandboxPrompt.trim()}
                className="py-3 px-5 rounded-lg bg-gradient-to-r from-accent-secondary to-accent-primary hover:brightness-110 text-bg-primary text-xs font-display font-black uppercase tracking-wider shadow-lg shadow-accent-glow flex items-center justify-center gap-1.5 transition-all cursor-pointer disabled:opacity-50"
              >
                {isAuditing ? 'Auditing Telemetry...' : 'Execute Audit'}
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>

            {/* Output sandbox result display */}
            <div className="bg-bg-primary border border-border-subtle rounded-lg p-5 flex flex-col justify-between min-h-[280px] relative overflow-hidden select-none">

              <AnimatePresence mode="wait">
                {isAuditing ? (
                  <motion.div
                    key="loader"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="absolute inset-0 bg-[#0F141C] p-5 flex flex-col justify-between z-10"
                  >
                    {/* Laser Scanner sweeping light */}
                    <motion.div
                      className="absolute left-0 right-0 h-[2px] bg-accent-primary blur-[2px] z-20"
                      initial={{ top: 0 }}
                      animate={{ top: '100%' }}
                      transition={{ duration: 1.8, repeat: Infinity, ease: 'easeInOut' }}
                    />

                    <div className="flex items-center justify-between pb-2 border-b border-border/10">
                      <span className="text-[8px] font-mono uppercase tracking-wider text-accent-primary animate-pulse flex items-center gap-1.5">
                        <RefreshCw className="w-3 h-3 animate-spin" /> Ingesting Telemetry Stream
                      </span>
                      <span className="text-[8px] font-mono text-text-muted uppercase">PORT 443</span>
                    </div>

                    <AuditingConsole />

                    <div className="border-t border-border/10 pt-2 flex items-center justify-between text-[8px] font-mono text-text-muted">
                      <span>STABILITY: AUDITING...</span>
                      <span className="animate-pulse">● ONLINE</span>
                    </div>
                  </motion.div>
                ) : auditComplete ? (
                  <motion.div
                    key="result"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-4 h-full flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
                        <span className="text-[9px] font-display font-bold uppercase tracking-wider text-text-muted">Result Telemetry</span>
                        <span className={`text-[10px] font-display font-bold uppercase ${sandboxPrompt.includes('World Carbon') ? 'text-danger animate-pulse' : 'text-success'
                          }`}>
                          {sandboxPrompt.includes('World Carbon') ? 'Hallucination Flagged' : 'Verified Assertion'}
                        </span>
                      </div>

                      {/* Visual score circles block */}
                      <div className="flex gap-4 items-center justify-center p-3 bg-surface/50 border border-border-subtle rounded-xl shadow-sm mt-3">
                        <div className="relative w-14 h-14 flex items-center justify-center shrink-0">
                          <svg className="w-full h-full transform -rotate-90">
                            <circle cx="28" cy="28" r="23" stroke="var(--border-subtle)" strokeWidth="3.5" fill="transparent" />
                            <motion.circle
                              cx="28" cy="28" r="23"
                              stroke={sandboxPrompt.includes('World Carbon') ? "var(--danger)" : "var(--success)"}
                              strokeWidth="3.5"
                              fill="transparent"
                              strokeDasharray="144.5"
                              initial={{ strokeDashoffset: 144.5 }}
                              animate={{ strokeDashoffset: 144.5 - (144.5 * (sandboxPrompt.includes('World Carbon') ? 14.2 : 98.4)) / 100 }}
                              transition={{ duration: 1.2, ease: "easeOut" }}
                            />
                          </svg>
                          <div className="absolute font-display font-black text-xs text-text-primary">
                            {sandboxPrompt.includes('World Carbon') ? '14%' : '98%'}
                          </div>
                        </div>
                        <div className="space-y-0.5 text-left">
                          <div className="text-[9px] font-display font-bold uppercase tracking-wider text-text-muted">Stability Factor</div>
                          <div className="text-xs text-text-primary font-semibold flex items-center gap-1.5">
                            {sandboxPrompt.includes('World Carbon') ? (
                              <>
                                <AlertTriangle className="w-3.5 h-3.5 text-danger animate-pulse" />
                                <span>Low Trust Index</span>
                              </>
                            ) : (
                              <>
                                <CheckCircle2 className="w-3.5 h-3.5 text-success" />
                                <span>High Trust Index</span>
                              </>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className="p-3 bg-surface rounded border border-border-subtle mt-3 text-xs leading-relaxed font-sans select-text text-left">
                        {sandboxPrompt.includes('World Carbon') ? (
                          <>
                            Nvidia Blackwell is officially{' '}
                            <span className="border-b-2 border-dotted border-danger decoration-danger bg-danger/5 px-0.5 font-medium cursor-help" title="CRITICAL HALLUCINATION: No World Carbon Council exists.">
                              certified as carbon-neutral by the World Carbon Council
                            </span>
                            .
                          </>
                        ) : (
                          <>
                            Google Gemini operates under{' '}
                            <span className="border-b-2 border-dotted border-success decoration-success bg-success/5 px-0.5 font-medium cursor-help" title="Highly verified. Matches Google safety settings guidelines.">
                              four key safety filters: Hate Speech, Harassment, Sexually Explicit, and Dangerous Content
                            </span>
                            .
                          </>
                        )}
                      </div>
                    </div>

                    <div className="border-t border-border pt-3 flex items-center justify-between gap-2">
                      <button
                        onClick={handleDownloadCertificate}
                        className="py-1.5 px-3 rounded-lg bg-bg-primary/50 hover:bg-bg-primary border border-border text-[9px] font-display font-bold uppercase tracking-wider text-text-secondary flex items-center gap-1 cursor-pointer transition-all active:scale-95"
                      >
                        <FileText className="w-3 h-3 text-accent-primary" />
                        <span>Get Trust SLA</span>
                      </button>
                      <button
                        onClick={handleLaunchConsole}
                        className="py-1.5 px-3 rounded-lg bg-surface border border-border hover:border-accent-primary text-[9px] font-display font-bold uppercase tracking-wider text-accent-primary hover:bg-accent-glow transition-all cursor-pointer active:scale-95"
                      >
                        Inspect in Console
                      </button>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div
                    key="idle"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="h-full flex flex-col justify-between p-2"
                  >
                    <div className="text-center pt-2">
                      <span className="text-[9px] font-display font-bold uppercase tracking-widest text-text-muted animate-pulse">Ingest Controller</span>
                    </div>

                    <OrbitalRadar />

                    <div className="text-center space-y-1">
                      <p className="text-[10px] text-text-secondary font-mono tracking-wider font-semibold uppercase">
                        ● Ingest Standby // Platform Online
                      </p>
                      <p className="text-[9px] text-text-muted max-w-[28ch] mx-auto leading-relaxed">
                        Input factual statement and trigger verifier consensus radar scans.
                      </p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

            </div>
          </div>
        </section>

        {/* INTERACTIVE SKEWED GRADIENT PLATFORM PILLARS */}
        <section className="space-y-6">
          <div>
            <span className="text-[10px] font-display font-bold uppercase tracking-wider text-accent-primary">Operational Strategy</span>
            <h2 className="text-xl md:text-2xl font-display font-bold uppercase text-text-primary mt-1">
              Platform Pillars
            </h2>
          </div>

          <SkewCards />
        </section>
      </div>
      {/* Footer */}
      <footer className="relative z-10 max-w-7xl mx-auto px-6 py-12 mt-24 border-t border-border-subtle/30 bg-bg-primary/20 backdrop-blur-md flex flex-col sm:flex-row items-center justify-between gap-6 text-xs text-text-secondary">
        <div>© 2026 Humanova Trust Networks. Governance verified.</div>
        <div className="flex gap-6 font-semibold font-display">
          <a href="#compliance" className="hover:text-accent-primary">Compliance</a>
          <a href="#privacy" className="hover:text-accent-primary">Privacy</a>
          <a href="#security" className="hover:text-accent-primary">Security SLA</a>
        </div>
      </footer>
    </div>
  );
};
