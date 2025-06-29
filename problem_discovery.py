import os
import json
import random
import time
from typing import List, Dict, Optional, Tuple
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import hashlib

class ProblemDiscoverer:
    def __init__(self, cache_dir: str = "data/discovered_problems"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.search_engines = [
            self._search_math_isfun,
            self._search_khan_academy,
            self._search_math_drill
        ]
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
    
    def _get_cache_file(self, query: str) -> str:
        """Get cache file path for a query."""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{query_hash}.json")
    
    def _load_from_cache(self, query: str) -> Optional[List[Dict]]:
        """Load search results from cache if available."""
        cache_file = self._get_cache_file(query)
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def _save_to_cache(self, query: str, results: List[Dict]):
        """Save search results to cache."""
        cache_file = self._get_cache_file(query)
        with open(cache_file, 'w') as f:
            json.dump(results, f, indent=2)
    
    def _make_request(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """Make HTTP request with rate limiting and error handling."""
        if headers is None:
            headers = {}
        
        headers['User-Agent'] = random.choice(self.user_agents)
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def _search_math_isfun(self, topic: str, grade: str) -> List[Dict]:
        """Search for problems on MathsIsFun.com."""
        query = f"{topic} grade {grade} site:mathsisfun.com"
        cache = self._load_from_cache(query)
        if cache is not None:
            return cache
        
        search_url = f"https://www.mathsisfun.com/search/\
                      search.html?q={quote_plus(topic)}&grade={grade}"
        
        html = self._make_request(search_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # Extract problems from search results
        for result in soup.select('.search-result'):
            title = result.select_one('h3')
            link = result.select_one('a')
            if title and link:
                results.append({
                    'source': 'MathIsFun',
                    'title': title.text.strip(),
                    'url': 'https://www.mathsisfun.com' + link['href'],
                    'difficulty': 'medium',
                    'topic': topic,
                    'subtopic': 'General',
                    'problem_type': 'word_problem'
                })
        
        self._save_to_cache(query, results)
        return results
    
    def _search_khan_academy(self, topic: str, grade: str) -> List[Dict]:
        """Search for problems on Khan Academy."""
        query = f"{topic} grade {grade} site:khanacademy.org"
        cache = self._load_from_cache(query)
        if cache is not None:
            return cache
        
        search_url = f"https://www.khanacademy.org/search?page_search_query={quote_plus(topic)}%20grade%20{grade}"
        
        # Note: Khan Academy requires proper API usage, this is a simplified version
        # In production, you'd want to use their official API
        results = []
        self._save_to_cache(query, results)
        return results
    
    def _search_math_drill(self, topic: str, grade: str) -> List[Dict]:
        """Search for problems on Math-Drills.com."""
        query = f"{topic} grade {grade} worksheet site:math-drills.com"
        cache = self._load_from_cache(query)
        if cache is not None:
            return cache
        
        search_url = f"https://www.math-drills.com/search.php?s={quote_plus(topic)}&grade={grade}"
        
        html = self._make_request(search_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # Extract problems from search results
        for result in soup.select('.search-results a'):
            if 'href' in result.attrs:
                results.append({
                    'source': 'MathDrills',
                    'title': result.text.strip(),
                    'url': 'https://www.math-drills.com' + result['href'],
                    'difficulty': 'medium',
                    'topic': topic,
                    'subtopic': 'Practice',
                    'problem_type': 'worksheet'
                })
        
        self._save_to_cache(query, results)
        return results
    
    def discover_new_problems(self, topic: str, grade: str, max_results: int = 10) -> List[Dict]:
        """Search multiple sources for new problem types."""
        all_results = []
        
        for search_func in self.search_engines:
            try:
                results = search_func(topic, grade)
                all_results.extend(results)
                if len(all_results) >= max_results:
                    break
                time.sleep(1)  # Be nice to servers
            except Exception as e:
                print(f"Error in {search_func.__name__}: {e}")
        
        # Deduplicate results
        seen = set()
        unique_results = []
        for result in all_results:
            result_id = hashlib.md5(
                (result.get('title', '') + result.get('url', '')).encode()
            ).hexdigest()
            if result_id not in seen:
                seen.add(result_id)
                unique_results.append(result)
        
        return unique_results[:max_results]
    
    def analyze_problem_patterns(self, problems: List[Dict]) -> Dict:
        """Analyze discovered problems to identify new patterns."""
        if not problems:
            return {}
        
        # Count problem types
        type_counts = {}
        sources = set()
        
        for problem in problems:
            prob_type = problem.get('problem_type', 'unknown')
            type_counts[prob_type] = type_counts.get(prob_type, 0) + 1
            sources.add(problem.get('source', 'unknown'))
        
        return {
            'total_problems': len(problems),
            'problem_types': type_counts,
            'sources': list(sources),
            'difficulty_distribution': {
                'easy': len([p for p in problems if p.get('difficulty') == 'easy']),
                'medium': len([p for p in problems if p.get('difficulty') == 'medium']),
                'hard': len([p for p in problems if p.get('difficulty') == 'hard']),
                'unknown': len([p for p in problems if 'difficulty' not in p])
            }
        }
