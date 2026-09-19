export type Lang = 'en' | 'zh' | 'ja' | 'es' | 'pt' | 'de';
export type Tier = 'core' | 'extended' | 'mixed' | 'verbose';

export interface Kaomoji {
  /** Stable identifier, e.g. "kao_000001". */
  id: string;
  /** The kaomoji itself. */
  text: string;
  category: string;
  /** English controlled-vocabulary emotion labels. */
  emotion: string[];
  /** English controlled-vocabulary intent labels (greeting, apology, ...). */
  intent: string[];
  /** English controlled-vocabulary subject labels (animal, food, ...). */
  subject: string[];
  /** Human-readable name per language. */
  names: Partial<Record<Lang, string>>;
  /** Search keywords per language. */
  keywords: Partial<Record<Lang, string[]>>;
  /** "traditional" for community kaomoji, "fontvibe-original" for our own designs. */
  origin: 'traditional' | 'fontvibe-original';
  /** ["*"] when suitable for every locale, otherwise e.g. ["ja"]. */
  locale_scope: string[];
  tier: Tier;
  sources: string[];
  ascii_safe: boolean;
  needs_cjk_font: boolean;
  display_width: number;
  length: number;
}

export interface Stats {
  total: number;
  core: number;
  originals: number;
  tiers: Record<Tier, number>;
  langs: Lang[];
  tagged: number;
}

export interface FilterOptions { limit?: number; tier?: Tier }
export interface SearchOptions extends FilterOptions { lang?: Lang }
export interface RandomOptions { category?: string; emotion?: string; tier?: Tier }

/** Parses the whole dataset once and caches it (~0.6s, ~200 MB resident). */
export function all(): Kaomoji[];
export function search(query: string, opts?: SearchOptions): Kaomoji[];
export function byCategory(category: string, opts?: FilterOptions): Kaomoji[];
export function byEmotion(emotion: string, opts?: FilterOptions): Kaomoji[];
export function random(opts?: RandomOptions): Kaomoji | null;
export function categories(): Array<{ name: string; count: number }>;
export function originals(): Kaomoji[];
export const stats: Stats;
export const LANGS: Lang[];
