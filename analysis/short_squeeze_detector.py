"""
Short Squeeze Detection Algorithm
Analyzes stocks for short squeeze potential based on multiple criteria
"""
import logging
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
import config

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class ShortSqueezeDetector:
    def __init__(self):
        self.weights = {
            'short_interest': 0.25,     # Short interest percentage
            'days_to_cover': 0.20,      # Days to cover ratio
            'cost_to_borrow': 0.15,     # Cost to borrow shares
            'volume_spike': 0.15,       # Volume vs average volume
            'price_momentum': 0.10,     # Recent price movement
            'float_size': 0.10,         # Size of public float
            'insider_ownership': 0.05   # Insider ownership percentage
        }
    
    def calculate_squeeze_score(self, stock_data: Dict) -> float:
        """Calculate overall squeeze potential score (0-100)"""
        try:
            scores = {}
            
            # Short Interest Score (0-25 points)
            short_interest = stock_data.get('short_percent_float', 0)
            scores['short_interest'] = min(short_interest * 1.25, 25)  # 20% short = 25 points
            
            # Days to Cover Score (0-20 points) 
            days_to_cover = stock_data.get('short_ratio', 0)
            if days_to_cover >= 10:
                scores['days_to_cover'] = 20
            elif days_to_cover >= 5:
                scores['days_to_cover'] = 15
            elif days_to_cover >= 3:
                scores['days_to_cover'] = 10
            else:
                scores['days_to_cover'] = days_to_cover * 3.33
            
            # Cost to Borrow Score (0-15 points)
            # Estimated based on short interest (higher short interest = higher borrow cost)
            estimated_ctb = min(short_interest * 2, 100)  # Rough estimation
            scores['cost_to_borrow'] = min(estimated_ctb * 0.15, 15)
            
            # Volume Spike Score (0-15 points)
            volume_ratio = stock_data.get('volume_ratio', 1)
            rel_volume = stock_data.get('rel_volume', 1)
            volume_score = max(volume_ratio, rel_volume)
            scores['volume_spike'] = min(volume_score * 3, 15)  # 5x volume = 15 points
            
            # Price Momentum Score (0-10 points)
            daily_change = stock_data.get('daily_change', 0)
            if daily_change > 0:
                scores['price_momentum'] = min(daily_change * 0.5, 10)  # 20% gain = 10 points
            else:
                scores['price_momentum'] = 0
            
            # Float Size Score (0-10 points) - smaller float = higher score
            market_cap = stock_data.get('market_cap', config.SMALL_CAP_MAX)
            if market_cap <= 500_000_000:  # Under $500M
                scores['float_size'] = 10
            elif market_cap <= 1_000_000_000:  # Under $1B
                scores['float_size'] = 7
            elif market_cap <= 1_500_000_000:  # Under $1.5B
                scores['float_size'] = 4
            else:
                scores['float_size'] = 2
            
            # Insider Ownership Score (0-5 points)
            insider_own = stock_data.get('insider_own', 0)
            scores['insider_ownership'] = min(insider_own * 0.25, 5)  # 20% insider = 5 points
            
            # Calculate total score
            total_score = sum(scores.values())
            
            # Store individual scores for analysis
            stock_data['squeeze_scores'] = scores
            stock_data['squeeze_score'] = round(total_score, 2)
            
            return total_score
            
        except Exception as e:
            logger.error(f"Error calculating squeeze score: {e}")
            return 0.0
    
    def analyze_squeeze_potential(self, stock_data: Dict) -> Dict:
        """Detailed analysis of short squeeze potential"""
        try:
            score = self.calculate_squeeze_score(stock_data)
            
            # Determine risk level
            if score >= 70:
                risk_level = "Very High"
                description = "Extremely high short squeeze potential"
            elif score >= 50:
                risk_level = "High" 
                description = "High short squeeze potential"
            elif score >= 30:
                risk_level = "Medium"
                description = "Moderate short squeeze potential"
            elif score >= 15:
                risk_level = "Low"
                description = "Low short squeeze potential"
            else:
                risk_level = "Very Low"
                description = "Minimal short squeeze potential"
            
            # Key factors analysis
            factors = []
            scores = stock_data.get('squeeze_scores', {})
            
            if scores.get('short_interest', 0) >= 15:
                factors.append(f"High short interest ({stock_data.get('short_percent_float', 0):.1f}%)")
            
            if scores.get('days_to_cover', 0) >= 15:
                factors.append(f"High days to cover ({stock_data.get('short_ratio', 0):.1f} days)")
            
            if scores.get('volume_spike', 0) >= 10:
                factors.append(f"Volume spike ({stock_data.get('volume_ratio', 1):.1f}x normal)")
            
            if scores.get('price_momentum', 0) >= 5:
                factors.append(f"Strong momentum ({stock_data.get('daily_change', 0):.1f}% today)")
            
            if scores.get('float_size', 0) >= 7:
                factors.append("Small float size")
            
            analysis = {
                'symbol': stock_data.get('symbol', 'N/A'),
                'squeeze_score': score,
                'risk_level': risk_level,
                'description': description,
                'key_factors': factors,
                'short_interest': stock_data.get('short_percent_float', 0),
                'days_to_cover': stock_data.get('short_ratio', 0),
                'market_cap': stock_data.get('market_cap', 0),
                'daily_change': stock_data.get('daily_change', 0),
                'volume_ratio': stock_data.get('volume_ratio', 1),
                'recommendation': self._get_recommendation(score, stock_data)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in squeeze analysis: {e}")
            return {}
    
    def rank_squeeze_candidates(self, stocks: List[Dict]) -> List[Dict]:
        """Rank stocks by squeeze potential"""
        try:
            # Calculate scores for all stocks
            for stock in stocks:
                self.calculate_squeeze_score(stock)
            
            # Filter stocks meeting minimum criteria
            candidates = []
            for stock in stocks:
                short_interest = stock.get('short_percent_float', 0)
                market_cap = stock.get('market_cap', 0)
                
                if (short_interest >= config.MIN_SHORT_INTEREST and
                    config.SMALL_CAP_MIN <= market_cap <= config.SMALL_CAP_MAX):
                    
                    analysis = self.analyze_squeeze_potential(stock)
                    if analysis:
                        candidates.append({**stock, **analysis})
            
            # Sort by squeeze score descending
            candidates.sort(key=lambda x: x.get('squeeze_score', 0), reverse=True)
            
            return candidates[:config.TOP_SQUEEZE_CANDIDATES]
            
        except Exception as e:
            logger.error(f"Error ranking squeeze candidates: {e}")
            return []
    
    def _get_recommendation(self, score: float, stock_data: Dict) -> str:
        """Generate trading recommendation based on analysis"""
        try:
            symbol = stock_data.get('symbol', 'N/A')
            short_interest = stock_data.get('short_percent_float', 0)
            daily_change = stock_data.get('daily_change', 0)
            volume_ratio = stock_data.get('volume_ratio', 1)
            
            if score >= 70:
                if daily_change > 10 and volume_ratio > 3:
                    return f"⚠️ EXTREME CAUTION: {symbol} showing potential squeeze signals but already moving rapidly"
                else:
                    return f"🎯 WATCH CLOSELY: {symbol} has very high squeeze potential"
            elif score >= 50:
                if volume_ratio > 2:
                    return f"📈 MONITOR: {symbol} showing increased activity with high squeeze potential"
                else:
                    return f"👀 INTERESTING: {symbol} has good squeeze setup"
            elif score >= 30:
                return f"📊 RESEARCH: {symbol} has moderate squeeze potential, worth investigating"
            else:
                return f"💭 LOW PRIORITY: {symbol} has limited squeeze potential"
                
        except Exception as e:
            logger.error(f"Error generating recommendation: {e}")
            return "Error generating recommendation"
    
    def detect_squeeze_in_progress(self, stock_data: Dict) -> bool:
        """Detect if a squeeze may already be happening"""
        try:
            daily_change = stock_data.get('daily_change', 0)
            volume_ratio = stock_data.get('volume_ratio', 1)
            short_interest = stock_data.get('short_percent_float', 0)
            
            # Criteria for squeeze in progress
            if (daily_change > 15 and          # Large price movement
                volume_ratio > 5 and           # Massive volume spike  
                short_interest > 15):          # High short interest
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error detecting squeeze in progress: {e}")
            return False