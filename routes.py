import hashlib
import random
import re
from datetime import datetime, date, timedelta
from flask import render_template, request, redirect, url_for, make_response
from app import app

# Performance optimizations in app.py handle headers

# Country data with enhanced SEO information (100 countries)
COUNTRIES = [
    {
        'code': 'US', 'name': 'United States', 'flag': '🇺🇸',
        'keywords': ['US virtual number', 'American SMS receiver', 'United States phone verification', 'US OTP service'],
        'region': 'North America', 'timezone': 'UTC-5 to UTC-8',
        'seo_description': 'Premium US virtual phone numbers for instant SMS verification. Reliable American numbers for secure account registration and testing.',
        'content_focus': 'banking verification', 'use_cases': ['financial apps', 'social media', 'e-commerce platforms']
    },
    {
        'code': 'GB', 'name': 'United Kingdom', 'flag': '🇬🇧',
        'keywords': ['UK virtual number', 'British SMS service', 'United Kingdom verification', 'GB phone receiver'],
        'region': 'Europe', 'timezone': 'UTC+0',
        'seo_description': 'Trusted UK virtual phone numbers for SMS verification. British numbers for secure online registration and development testing.',
        'content_focus': 'digital services', 'use_cases': ['fintech apps', 'gaming platforms', 'business tools']
    },
    {
        'code': 'FR', 'name': 'France', 'flag': '🇫🇷',
        'keywords': ['France virtual number', 'French SMS receiver', 'FR phone verification', 'French OTP numbers'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Secure French virtual phone numbers for SMS verification. Premium France numbers for reliable message reception and testing.',
        'content_focus': 'e-commerce verification', 'use_cases': ['online shopping', 'travel apps', 'delivery services']
    },
    {
        'code': 'DE', 'name': 'Germany', 'flag': '🇩🇪',
        'keywords': ['Germany virtual number', 'German SMS service', 'DE phone verification', 'German OTP receiver'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Professional German virtual phone numbers for SMS verification. Reliable DE numbers for secure account creation and API testing.',
        'content_focus': 'business verification', 'use_cases': ['enterprise apps', 'logistics platforms', 'tech startups']
    },
    {
        'code': 'IT', 'name': 'Italy', 'flag': '🇮🇹',
        'keywords': ['Italy virtual number', 'Italian SMS receiver', 'IT phone verification', 'Italian OTP service'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Quality Italian virtual phone numbers for SMS verification. Trusted IT numbers for online registration and development projects.',
        'content_focus': 'social media verification', 'use_cases': ['social platforms', 'dating apps', 'communication tools']
    },
    {
        'code': 'ES', 'name': 'Spain', 'flag': '🇪🇸',
        'keywords': ['Spain virtual number', 'Spanish SMS service', 'ES phone verification', 'Spanish OTP numbers'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Reliable Spanish virtual phone numbers for SMS verification. Premium ES numbers for secure messaging and application testing.',
        'content_focus': 'travel verification', 'use_cases': ['booking platforms', 'travel apps', 'hospitality services']
    },
    {
        'code': 'CA', 'name': 'Canada', 'flag': '🇨🇦',
        'keywords': ['Canada virtual number', 'Canadian SMS receiver', 'CA phone verification', 'Canadian OTP service'],
        'region': 'North America', 'timezone': 'UTC-3.5 to UTC-8',
        'seo_description': 'Premium Canadian virtual phone numbers for SMS verification. Trusted CA numbers for secure account setup and testing workflows.',
        'content_focus': 'healthcare verification', 'use_cases': ['health apps', 'insurance platforms', 'government services']
    },
    {
        'code': 'AU', 'name': 'Australia', 'flag': '🇦🇺',
        'keywords': ['Australia virtual number', 'Australian SMS service', 'AU phone verification', 'Aussie OTP numbers'],
        'region': 'Oceania', 'timezone': 'UTC+8 to UTC+11',
        'seo_description': 'Professional Australian virtual phone numbers for SMS verification. Reliable AU numbers for secure registration and development testing.',
        'content_focus': 'educational verification', 'use_cases': ['learning platforms', 'university apps', 'student services']
    },
    {
        'code': 'JP', 'name': 'Japan', 'flag': '🇯🇵',
        'keywords': ['Japan virtual number', 'Japanese SMS receiver', 'JP phone verification', 'Japanese OTP service'],
        'region': 'Asia', 'timezone': 'UTC+9',
        'seo_description': 'Advanced Japanese virtual phone numbers for SMS verification. Premium JP numbers for secure authentication and mobile testing.',
        'content_focus': 'gaming verification', 'use_cases': ['mobile games', 'entertainment apps', 'tech platforms']
    },
    {
        'code': 'KR', 'name': 'South Korea', 'flag': '🇰🇷',
        'keywords': ['Korea virtual number', 'Korean SMS service', 'KR phone verification', 'Korean OTP receiver'],
        'region': 'Asia', 'timezone': 'UTC+9',
        'seo_description': 'High-tech Korean virtual phone numbers for SMS verification. Reliable KR numbers for secure digital services and app development.',
        'content_focus': 'tech verification', 'use_cases': ['tech startups', 'mobile apps', 'digital services']
    },
    {
        'code': 'CN', 'name': 'China', 'flag': '🇨🇳',
        'keywords': ['China virtual number', 'Chinese SMS receiver', 'CN phone verification', 'Chinese OTP service'],
        'region': 'Asia', 'timezone': 'UTC+8',
        'seo_description': 'Secure Chinese virtual phone numbers for SMS verification. Professional CN numbers for reliable authentication and testing purposes.',
        'content_focus': 'marketplace verification', 'use_cases': ['e-commerce sites', 'payment apps', 'trading platforms']
    },
    {
        'code': 'IN', 'name': 'India', 'flag': '🇮🇳',
        'keywords': ['India virtual number', 'Indian SMS service', 'IN phone verification', 'Bharat OTP numbers'],
        'region': 'Asia', 'timezone': 'UTC+5:30',
        'seo_description': 'Reliable Indian virtual phone numbers for SMS verification. Trusted IN numbers for secure registration and mobile app development.',
        'content_focus': 'startup verification', 'use_cases': ['fintech startups', 'ride-sharing apps', 'food delivery platforms']
    },
    {
        'code': 'BR', 'name': 'Brazil', 'flag': '🇧🇷',
        'keywords': ['Brazil virtual number', 'Brazilian SMS receiver', 'BR phone verification', 'Brazilian OTP service'],
        'region': 'South America', 'timezone': 'UTC-3',
        'seo_description': 'Premium Brazilian virtual phone numbers for SMS verification. Quality BR numbers for secure online services and application testing.',
        'content_focus': 'sports verification', 'use_cases': ['sports betting', 'fantasy sports', 'gaming platforms']
    },
    {
        'code': 'MX', 'name': 'Mexico', 'flag': '🇲🇽',
        'keywords': ['Mexico virtual number', 'Mexican SMS service', 'MX phone verification', 'Mexican OTP receiver'],
        'region': 'North America', 'timezone': 'UTC-6 to UTC-8',
        'seo_description': 'Professional Mexican virtual phone numbers for SMS verification. Reliable MX numbers for secure authentication and development testing.',
        'content_focus': 'remittance verification', 'use_cases': ['money transfer apps', 'banking services', 'payment platforms']
    },
    {
        'code': 'RU', 'name': 'Russia', 'flag': '🇷🇺',
        'keywords': ['Russia virtual number', 'Russian SMS receiver', 'RU phone verification', 'Russian OTP service'],
        'region': 'Europe/Asia', 'timezone': 'UTC+3 to UTC+12',
        'seo_description': 'Advanced Russian virtual phone numbers for SMS verification. Premium RU numbers for secure digital services and software testing.',
        'content_focus': 'energy verification', 'use_cases': ['energy platforms', 'industrial apps', 'logistics services']
    },
    {
        'code': 'NL', 'name': 'Netherlands', 'flag': '🇳🇱',
        'keywords': ['Netherlands virtual number', 'Dutch SMS service', 'NL phone verification', 'Holland OTP numbers'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Quality Dutch virtual phone numbers for SMS verification. Trusted NL numbers for secure online registration and API development.',
        'content_focus': 'cycling verification', 'use_cases': ['bike-sharing apps', 'transportation platforms', 'mobility services']
    },
    {
        'code': 'BE', 'name': 'Belgium', 'flag': '🇧🇪',
        'keywords': ['Belgium virtual number', 'Belgian SMS receiver', 'BE phone verification', 'Belgian OTP service'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Professional Belgian virtual phone numbers for SMS verification. Reliable BE numbers for secure authentication and testing workflows.',
        'content_focus': 'chocolate verification', 'use_cases': ['food delivery apps', 'restaurant platforms', 'culinary services']
    },
    {
        'code': 'CH', 'name': 'Switzerland', 'flag': '🇨🇭',
        'keywords': ['Switzerland virtual number', 'Swiss SMS service', 'CH phone verification', 'Swiss OTP receiver'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Premium Swiss virtual phone numbers for SMS verification. High-quality CH numbers for secure financial services and app testing.',
        'content_focus': 'finance verification', 'use_cases': ['banking apps', 'investment platforms', 'crypto services']
    },
    {
        'code': 'AT', 'name': 'Austria', 'flag': '🇦🇹',
        'keywords': ['Austria virtual number', 'Austrian SMS receiver', 'AT phone verification', 'Austrian OTP service'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Reliable Austrian virtual phone numbers for SMS verification. Quality AT numbers for secure registration and development projects.',
        'content_focus': 'music verification', 'use_cases': ['streaming apps', 'music platforms', 'entertainment services']
    },
    {
        'code': 'SE', 'name': 'Sweden', 'flag': '🇸🇪',
        'keywords': ['Sweden virtual number', 'Swedish SMS service', 'SE phone verification', 'Swedish OTP numbers'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Advanced Swedish virtual phone numbers for SMS verification. Premium SE numbers for secure Nordic services and mobile testing.',
        'content_focus': 'sustainability verification', 'use_cases': ['green tech apps', 'environmental platforms', 'clean energy services']
    },
    {
        'code': 'NO', 'name': 'Norway', 'flag': '🇳🇴',
        'keywords': ['Norway virtual number', 'Norwegian SMS receiver', 'NO phone verification', 'Norwegian OTP service'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Professional Norwegian virtual phone numbers for SMS verification. Trusted NO numbers for secure oil industry and maritime apps.',
        'content_focus': 'maritime verification', 'use_cases': ['shipping apps', 'maritime platforms', 'offshore services']
    },
    {
        'code': 'DK', 'name': 'Denmark', 'flag': '🇩🇰',
        'keywords': ['Denmark virtual number', 'Danish SMS service', 'DK phone verification', 'Danish OTP receiver'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Quality Danish virtual phone numbers for SMS verification. Reliable DK numbers for secure Scandinavian services and app development.',
        'content_focus': 'design verification', 'use_cases': ['design platforms', 'architecture apps', 'creative services']
    },
    {
        'code': 'FI', 'name': 'Finland', 'flag': '🇫🇮',
        'keywords': ['Finland virtual number', 'Finnish SMS receiver', 'FI phone verification', 'Finnish OTP service'],
        'region': 'Europe', 'timezone': 'UTC+2',
        'seo_description': 'Premium Finnish virtual phone numbers for SMS verification. High-tech FI numbers for secure Nordic tech services and testing.',
        'content_focus': 'gaming verification', 'use_cases': ['mobile games', 'gaming platforms', 'esports apps']
    },
    {
        'code': 'IE', 'name': 'Ireland', 'flag': '🇮🇪',
        'keywords': ['Ireland virtual number', 'Irish SMS service', 'IE phone verification', 'Irish OTP numbers'],
        'region': 'Europe', 'timezone': 'UTC+0',
        'seo_description': 'Trusted Irish virtual phone numbers for SMS verification. Professional IE numbers for secure European services and software testing.',
        'content_focus': 'tech verification', 'use_cases': ['tech companies', 'software platforms', 'cloud services']
    },
    {
        'code': 'PT', 'name': 'Portugal', 'flag': '🇵🇹',
        'keywords': ['Portugal virtual number', 'Portuguese SMS receiver', 'PT phone verification', 'Portuguese OTP service'],
        'region': 'Europe', 'timezone': 'UTC+0',
        'seo_description': 'Reliable Portuguese virtual phone numbers for SMS verification. Quality PT numbers for secure Iberian services and mobile development.',
        'content_focus': 'tourism verification', 'use_cases': ['travel booking', 'tourism apps', 'hospitality platforms']
    },
    {
        'code': 'GR', 'name': 'Greece', 'flag': '🇬🇷',
        'keywords': ['Greece virtual number', 'Greek SMS service', 'GR phone verification', 'Greek OTP receiver'],
        'region': 'Europe', 'timezone': 'UTC+2',
        'seo_description': 'Professional Greek virtual phone numbers for SMS verification. Trusted GR numbers for secure Mediterranean services and app testing.',
        'content_focus': 'shipping verification', 'use_cases': ['shipping platforms', 'logistics apps', 'maritime services']
    },
    {
        'code': 'PL', 'name': 'Poland', 'flag': '🇵🇱',
        'keywords': ['Poland virtual number', 'Polish SMS receiver', 'PL phone verification', 'Polish OTP service'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Advanced Polish virtual phone numbers for SMS verification. Premium PL numbers for secure Central European services and development.',
        'content_focus': 'manufacturing verification', 'use_cases': ['industrial apps', 'manufacturing platforms', 'supply chain services']
    },
    {
        'code': 'CZ', 'name': 'Czech Republic', 'flag': '🇨🇿',
        'keywords': ['Czech virtual number', 'Czech SMS service', 'CZ phone verification', 'Czech OTP numbers'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Quality Czech virtual phone numbers for SMS verification. Reliable CZ numbers for secure Central European apps and testing workflows.',
        'content_focus': 'beer verification', 'use_cases': ['beverage apps', 'restaurant platforms', 'food delivery services']
    },
    {
        'code': 'SK', 'name': 'Slovakia', 'flag': '🇸🇰',
        'keywords': ['Slovakia virtual number', 'Slovak SMS receiver', 'SK phone verification', 'Slovak OTP service'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Professional Slovak virtual phone numbers for SMS verification. Trusted SK numbers for secure Eastern European services and mobile testing.',
        'content_focus': 'automotive verification', 'use_cases': ['automotive apps', 'car sharing', 'transportation platforms']
    },
    {
        'code': 'HU', 'name': 'Hungary', 'flag': '🇭🇺',
        'keywords': ['Hungary virtual number', 'Hungarian SMS service', 'HU phone verification', 'Hungarian OTP receiver'],
        'region': 'Europe', 'timezone': 'UTC+1',
        'seo_description': 'Reliable Hungarian virtual phone numbers for SMS verification. Quality HU numbers for secure Central European services and app development.',
        'content_focus': 'thermal verification', 'use_cases': ['wellness apps', 'spa platforms', 'health services']
    },
    {'code': 'RO', 'name': 'Romania', 'flag': '🇷🇴'},
    {'code': 'BG', 'name': 'Bulgaria', 'flag': '🇧🇬'},
    {'code': 'HR', 'name': 'Croatia', 'flag': '🇭🇷'},
    {'code': 'SI', 'name': 'Slovenia', 'flag': '🇸🇮'},
    {'code': 'LT', 'name': 'Lithuania', 'flag': '🇱🇹'},
    {'code': 'LV', 'name': 'Latvia', 'flag': '🇱🇻'},
    {'code': 'EE', 'name': 'Estonia', 'flag': '🇪🇪'},
    {'code': 'IS', 'name': 'Iceland', 'flag': '🇮🇸'},
    {'code': 'MT', 'name': 'Malta', 'flag': '🇲🇹'},
    {'code': 'CY', 'name': 'Cyprus', 'flag': '🇨🇾'},
    {'code': 'LU', 'name': 'Luxembourg', 'flag': '🇱🇺'},
    {'code': 'TR', 'name': 'Turkey', 'flag': '🇹🇷'},
    {'code': 'IL', 'name': 'Israel', 'flag': '🇮🇱'},
    {'code': 'SA', 'name': 'Saudi Arabia', 'flag': '🇸🇦'},
    {'code': 'AE', 'name': 'UAE', 'flag': '🇦🇪'},
    {'code': 'QA', 'name': 'Qatar', 'flag': '🇶🇦'},
    {'code': 'KW', 'name': 'Kuwait', 'flag': '🇰🇼'},
    {'code': 'BH', 'name': 'Bahrain', 'flag': '🇧🇭'},
    {'code': 'OM', 'name': 'Oman', 'flag': '🇴🇲'},
    {'code': 'JO', 'name': 'Jordan', 'flag': '🇯🇴'},
    {'code': 'LB', 'name': 'Lebanon', 'flag': '🇱🇧'},
    {'code': 'EG', 'name': 'Egypt', 'flag': '🇪🇬'},
    {'code': 'MA', 'name': 'Morocco', 'flag': '🇲🇦'},
    {'code': 'DZ', 'name': 'Algeria', 'flag': '🇩🇿'},
    {'code': 'TN', 'name': 'Tunisia', 'flag': '🇹🇳'},
    {'code': 'ZA', 'name': 'South Africa', 'flag': '🇿🇦'},
    {'code': 'NG', 'name': 'Nigeria', 'flag': '🇳🇬'},
    {'code': 'KE', 'name': 'Kenya', 'flag': '🇰🇪'},
    {'code': 'GH', 'name': 'Ghana', 'flag': '🇬🇭'},
    {'code': 'UG', 'name': 'Uganda', 'flag': '🇺🇬'},
    {'code': 'TZ', 'name': 'Tanzania', 'flag': '🇹🇿'},
    {'code': 'ET', 'name': 'Ethiopia', 'flag': '🇪🇹'},
    {'code': 'MU', 'name': 'Mauritius', 'flag': '🇲🇺'},
    {'code': 'AR', 'name': 'Argentina', 'flag': '🇦🇷'},
    {'code': 'CL', 'name': 'Chile', 'flag': '🇨🇱'},
    {'code': 'CO', 'name': 'Colombia', 'flag': '🇨🇴'},
    {'code': 'PE', 'name': 'Peru', 'flag': '🇵🇪'},
    {'code': 'VE', 'name': 'Venezuela', 'flag': '🇻🇪'},
    {'code': 'UY', 'name': 'Uruguay', 'flag': '🇺🇾'},
    {'code': 'PY', 'name': 'Paraguay', 'flag': '🇵🇾'},
    {'code': 'BO', 'name': 'Bolivia', 'flag': '🇧🇴'},
    {'code': 'EC', 'name': 'Ecuador', 'flag': '🇪🇨'},
    {'code': 'GT', 'name': 'Guatemala', 'flag': '🇬🇹'},
    {'code': 'CR', 'name': 'Costa Rica', 'flag': '🇨🇷'},
    {'code': 'PA', 'name': 'Panama', 'flag': '🇵🇦'},
    {'code': 'DO', 'name': 'Dominican Republic', 'flag': '🇩🇴'},
    {'code': 'JM', 'name': 'Jamaica', 'flag': '🇯🇲'},
    {'code': 'TH', 'name': 'Thailand', 'flag': '🇹🇭'},
    {'code': 'VN', 'name': 'Vietnam', 'flag': '🇻🇳'},
    {'code': 'MY', 'name': 'Malaysia', 'flag': '🇲🇾'},
    {'code': 'SG', 'name': 'Singapore', 'flag': '🇸🇬'},
    {'code': 'PH', 'name': 'Philippines', 'flag': '🇵🇭'},
    {'code': 'ID', 'name': 'Indonesia', 'flag': '🇮🇩'},
    {'code': 'BD', 'name': 'Bangladesh', 'flag': '🇧🇩'},
    {'code': 'PK', 'name': 'Pakistan', 'flag': '🇵🇰'},
    {'code': 'LK', 'name': 'Sri Lanka', 'flag': '🇱🇰'},
    {'code': 'NP', 'name': 'Nepal', 'flag': '🇳🇵'},
    {'code': 'AF', 'name': 'Afghanistan', 'flag': '🇦🇫'},
    {'code': 'IR', 'name': 'Iran', 'flag': '🇮🇷'},
    {'code': 'IQ', 'name': 'Iraq', 'flag': '🇮🇶'},
    {'code': 'KZ', 'name': 'Kazakhstan', 'flag': '🇰🇿'},
    {'code': 'UZ', 'name': 'Uzbekistan', 'flag': '🇺🇿'},
    {'code': 'KG', 'name': 'Kyrgyzstan', 'flag': '🇰🇬'},
    {'code': 'TJ', 'name': 'Tajikistan', 'flag': '🇹🇯'},
    {'code': 'TM', 'name': 'Turkmenistan', 'flag': '🇹🇲'},
    {'code': 'MN', 'name': 'Mongolia', 'flag': '🇲🇳'},
    {'code': 'NZ', 'name': 'New Zealand', 'flag': '🇳🇿'},
    {'code': 'FJ', 'name': 'Fiji', 'flag': '🇫🇯'},
    {'code': 'PG', 'name': 'Papua New Guinea', 'flag': '🇵🇬'},
    {'code': 'NC', 'name': 'New Caledonia', 'flag': '🇳🇨'},
    {'code': 'UA', 'name': 'Ukraine', 'flag': '🇺🇦'},
    {'code': 'BY', 'name': 'Belarus', 'flag': '🇧🇾'},
    {'code': 'MD', 'name': 'Moldova', 'flag': '🇲🇩'},
    {'code': 'RS', 'name': 'Serbia', 'flag': '🇷🇸'},
    {'code': 'ME', 'name': 'Montenegro', 'flag': '🇲🇪'},
    {'code': 'BA', 'name': 'Bosnia and Herzegovina', 'flag': '🇧🇦'},
    {'code': 'MK', 'name': 'North Macedonia', 'flag': '🇲🇰'},
    {'code': 'AL', 'name': 'Albania', 'flag': '🇦🇱'},
]

def get_country_by_code(code):
    """Get country data by country code"""
    for country in COUNTRIES:
        if country['code'] == code.upper():
            return country
    return None

def generate_seo_data_for_country(country):
    """Generate SEO data for countries that don't have detailed info"""
    if 'keywords' in country:
        return country  # Already has SEO data
    
    # Generate default SEO data based on country name
    country_name = country['name']
    country_code = country['code']
    
    # Generate varied keywords to avoid duplication
    keywords = [
        f"{country_name} virtual number",
        f"{country_code} SMS receiver", 
        f"{country_name} phone verification",
        f"{country_code} OTP service"
    ]
    
    # Generate unique descriptions using different templates
    description_templates = [
        f"Professional {country_name} virtual phone numbers for SMS verification. Secure {country_code} numbers for reliable authentication and testing.",
        f"Premium {country_name} virtual numbers for SMS reception. Trusted {country_code} phone services for secure verification processes.",
        f"Quality {country_name} virtual phone numbers for SMS verification. Reliable {country_code} numbers for secure online registration.",
        f"Advanced {country_name} virtual phone numbers for SMS verification. Professional {country_code} numbers for secure digital services.",
        f"Secure {country_name} virtual phone numbers for SMS verification. Premium {country_code} numbers for reliable message reception."
    ]
    
    # Use hash of country code to select consistent template
    hash_val = hash(country_code) % len(description_templates)
    seo_description = description_templates[hash_val]
    
    # Generate region info
    regions = {
        'US': 'North America', 'CA': 'North America', 'MX': 'North America',
        'BR': 'South America', 'AR': 'South America', 'CL': 'South America', 'CO': 'South America',
        'PE': 'South America', 'VE': 'South America', 'UY': 'South America', 'PY': 'South America',
        'BO': 'South America', 'EC': 'South America',
        'GB': 'Europe', 'FR': 'Europe', 'DE': 'Europe', 'IT': 'Europe', 'ES': 'Europe',
        'NL': 'Europe', 'BE': 'Europe', 'CH': 'Europe', 'AT': 'Europe', 'SE': 'Europe',
        'NO': 'Europe', 'DK': 'Europe', 'FI': 'Europe', 'IE': 'Europe', 'PT': 'Europe',
        'GR': 'Europe', 'PL': 'Europe', 'CZ': 'Europe', 'SK': 'Europe', 'HU': 'Europe',
        'RO': 'Europe', 'BG': 'Europe', 'HR': 'Europe', 'SI': 'Europe', 'LT': 'Europe',
        'LV': 'Europe', 'EE': 'Europe', 'IS': 'Europe', 'MT': 'Europe', 'CY': 'Europe',
        'LU': 'Europe', 'TR': 'Europe/Asia', 'UA': 'Europe', 'BY': 'Europe', 'MD': 'Europe',
        'RS': 'Europe', 'ME': 'Europe', 'BA': 'Europe', 'MK': 'Europe', 'AL': 'Europe',
        'RU': 'Europe/Asia', 'KZ': 'Asia', 'UZ': 'Asia', 'KG': 'Asia', 'TJ': 'Asia',
        'TM': 'Asia', 'MN': 'Asia',
        'CN': 'Asia', 'JP': 'Asia', 'KR': 'Asia', 'IN': 'Asia', 'TH': 'Asia',
        'VN': 'Asia', 'MY': 'Asia', 'SG': 'Asia', 'PH': 'Asia', 'ID': 'Asia',
        'BD': 'Asia', 'PK': 'Asia', 'LK': 'Asia', 'NP': 'Asia', 'AF': 'Asia',
        'IR': 'Asia', 'IQ': 'Asia',
        'IL': 'Middle East', 'SA': 'Middle East', 'AE': 'Middle East', 'QA': 'Middle East',
        'KW': 'Middle East', 'BH': 'Middle East', 'OM': 'Middle East', 'JO': 'Middle East',
        'LB': 'Middle East',
        'EG': 'Africa', 'MA': 'Africa', 'DZ': 'Africa', 'TN': 'Africa', 'ZA': 'Africa',
        'NG': 'Africa', 'KE': 'Africa', 'GH': 'Africa', 'UG': 'Africa', 'TZ': 'Africa',
        'ET': 'Africa', 'MU': 'Africa',
        'AU': 'Oceania', 'NZ': 'Oceania', 'FJ': 'Oceania', 'PG': 'Oceania', 'NC': 'Oceania',
        'GT': 'Central America', 'CR': 'Central America', 'PA': 'Central America',
        'DO': 'Caribbean', 'JM': 'Caribbean'
    }
    
    # Generate varied content focus themes
    focus_themes = [
        'business verification', 'social verification', 'financial verification',
        'mobile verification', 'platform verification', 'service verification',
        'account verification', 'digital verification', 'secure verification'
    ]
    
    use_case_themes = [
        ['mobile apps', 'web services', 'digital platforms'],
        ['fintech apps', 'payment services', 'banking platforms'],
        ['social media', 'messaging apps', 'communication tools'],
        ['e-commerce sites', 'online stores', 'marketplace platforms'],
        ['travel apps', 'booking services', 'hospitality platforms'],
        ['gaming platforms', 'entertainment apps', 'media services'],
        ['business tools', 'enterprise apps', 'productivity platforms']
    ]
    
    hash_focus = hash(country_code + 'focus') % len(focus_themes)
    hash_use_case = hash(country_code + 'use_case') % len(use_case_themes)
    
    return {
        **country,
        'keywords': keywords,
        'region': regions.get(country_code, 'Global'),
        'timezone': f'UTC+{(hash(country_code) % 24) - 12}',  # Generate consistent timezone
        'seo_description': seo_description,
        'content_focus': focus_themes[hash_focus],
        'use_cases': use_case_themes[hash_use_case]
    }

def generate_phone_numbers(country_code, num_numbers=10):
    """Generate deterministic phone numbers for a country using seeded random"""
    today = date.today().strftime('%Y%m%d')
    seed = f"{country_code}{today}"
    random.seed(hashlib.md5(seed.encode()).hexdigest())
    
    numbers = []
    for i in range(num_numbers):
        # Generate realistic phone numbers based on country patterns
        if country_code == 'US':
            area = random.randint(200, 999)
            exchange = random.randint(200, 999)
            number_part = random.randint(1000, 9999)
            number = f"+1 {area} {exchange} {number_part}"
        elif country_code == 'GB':
            prefix = random.randint(7000, 7999)
            main = random.randint(100000, 999999)
            number = f"+44 {prefix} {main}"
        elif country_code == 'DE':
            area = random.randint(30, 89)
            main = random.randint(10000000, 99999999)
            number = f"+49 {area} {str(main)[:4]} {str(main)[4:]}"
        elif country_code == 'FR':
            prefix = random.randint(1, 9)
            main = random.randint(10000000, 99999999)
            number = f"+33 {prefix} {str(main)[:2]} {str(main)[2:4]} {str(main)[4:6]} {str(main)[6:]}"
        elif country_code == 'JP':
            area = random.randint(70, 90)
            main = random.randint(1000, 9999)
            last = random.randint(1000, 9999)
            number = f"+81 {area} {main} {last}"
        elif country_code == 'KR':
            prefix = random.randint(10, 19)
            main = random.randint(1000, 9999)
            last = random.randint(1000, 9999)
            number = f"+82 {prefix} {main} {last}"
        elif country_code == 'CN':
            area = random.randint(130, 199)
            main = random.randint(1000, 9999)
            last = random.randint(1000, 9999)
            number = f"+86 {area} {main} {last}"
        elif country_code == 'IN':
            area = random.randint(70, 99)
            main = random.randint(1000, 9999)
            last = random.randint(1000, 9999)
            number = f"+91 {area} {main} {last}"
        elif country_code == 'AU':
            area = random.randint(400, 499)
            main = random.randint(100, 999)
            last = random.randint(100, 999)
            number = f"+61 {area} {main} {last}"
        elif country_code == 'CA':
            area = random.randint(200, 999)
            exchange = random.randint(200, 999)
            number_part = random.randint(1000, 9999)
            number = f"+1 {area} {exchange} {number_part}"
        elif country_code == 'BR':
            area = random.randint(11, 99)
            prefix = random.randint(9, 9)
            main = random.randint(1000, 9999)
            last = random.randint(1000, 9999)
            number = f"+55 {area} {prefix} {main} {last}"
        elif country_code == 'IT':
            area = random.randint(300, 399)
            main = random.randint(100, 999)
            last = random.randint(1000, 9999)
            number = f"+39 {area} {main} {last}"
        elif country_code == 'ES':
            prefix = random.randint(6, 7)
            main = random.randint(10000000, 99999999)
            number = f"+34 {prefix} {str(main)[:2]} {str(main)[2:4]} {str(main)[4:6]} {str(main)[6:]}"
        elif country_code == 'NL':
            prefix = random.randint(6, 6)
            main = random.randint(10000000, 99999999)
            number = f"+31 {prefix} {str(main)[:4]} {str(main)[4:]}"
        elif country_code == 'RU':
            area = random.randint(900, 999)
            main = random.randint(100, 999)
            last = random.randint(10, 99)
            end = random.randint(10, 99)
            number = f"+7 {area} {main} {last} {end}"
        elif country_code == 'KZ':
            area = random.randint(700, 799)
            main = random.randint(100, 999)
            last = random.randint(1000, 9999)
            number = f"+7 {area} {main} {last}"
        else:
            # Generic international format with proper spacing
            country_codes = {
                'SE': 46, 'NO': 47, 'DK': 45, 'FI': 358, 'IE': 353, 'PT': 351,
                'GR': 30, 'PL': 48, 'CZ': 420, 'SK': 421, 'HU': 36, 'RO': 40,
                'BG': 359, 'HR': 385, 'SI': 386, 'LT': 370, 'LV': 371, 'EE': 372,
                'IS': 354, 'MT': 356, 'CY': 357, 'LU': 352, 'TR': 90, 'UA': 380,
                'BY': 375, 'MD': 373, 'RS': 381, 'ME': 382, 'BA': 387, 'MK': 389,
                'AL': 355, 'TH': 66, 'VN': 84, 'MY': 60, 'SG': 65, 'PH': 63,
                'ID': 62, 'BD': 880, 'PK': 92, 'LK': 94, 'NP': 977, 'AF': 93,
                'IR': 98, 'IQ': 964, 'UZ': 998, 'KG': 996, 'TJ': 992, 'TM': 993,
                'MN': 976, 'NZ': 64, 'FJ': 679, 'PG': 675, 'NC': 687, 'MX': 52,
                'AR': 54, 'CL': 56, 'CO': 57, 'PE': 51, 'VE': 58, 'UY': 598,
                'PY': 595, 'BO': 591, 'EC': 593, 'GT': 502, 'CR': 506, 'PA': 507,
                'DO': 1, 'JM': 1, 'IL': 972, 'SA': 966, 'AE': 971, 'QA': 974,
                'KW': 965, 'BH': 973, 'OM': 968, 'JO': 962, 'LB': 961, 'EG': 20,
                'MA': 212, 'DZ': 213, 'TN': 216, 'ZA': 27, 'NG': 234, 'KE': 254,
                'GH': 233, 'UG': 256, 'TZ': 255, 'ET': 251, 'MU': 230
            }
            
            code = country_codes.get(country_code, random.randint(1, 999))
            main = random.randint(100000000, 999999999)
            if len(str(main)) == 9:
                number = f"+{code} {str(main)[:3]} {str(main)[3:6]} {str(main)[6:]}"
            else:
                number = f"+{code} {str(main)[:4]} {str(main)[4:]}"
        
        # Random status - roughly 70% live, 30% offline
        status = 'live' if random.random() < 0.7 else 'offline'
        
        numbers.append({
            'number': number,
            'status': status
        })
    
    return numbers

def generate_messages(country_code, phone_number, num_messages=15):
    """Generate fake SMS messages for a phone number"""
    today = date.today().strftime('%Y%m%d')
    seed = f"{country_code}{phone_number}{today}"
    random.seed(hashlib.md5(seed.encode()).hexdigest())
    
    message_templates = [
        "Your verification code is {code}. Valid for 10 minutes.",
        "Welcome! Your account has been created. Code: {code}",
        "Your login code is {code}. Do not share this code.",
        "Bank Alert: Transaction of ${amount} processed. Code: {code}",
        "Your delivery is scheduled for today. Track with code: {code}",
        "Password reset requested. Use code {code} to proceed.",
        "Your ride is arriving in 5 minutes. Driver code: {code}",
        "Confirmation code for your order: {code}",
        "Security alert: New login detected. Code: {code}",
        "Your appointment is confirmed. Reference: {code}",
        "Payment received! Transaction ID: {code}",
        "Welcome to our service! Activation code: {code}",
        "Your subscription is active. Code: {code}",
        "Order shipped! Tracking number: {code}",
        "Account verification required. Code: {code}",
    ]
    
    companies = [
        "Amazon", "Google", "Microsoft", "Apple", "PayPal", "Uber", "DoorDash",
        "Netflix", "Spotify", "WhatsApp", "Facebook", "Twitter", "Instagram",
        "LinkedIn", "Discord", "Telegram", "Signal", "Chase Bank", "Wells Fargo",
        "BankOfAmerica", "Visa", "Mastercard", "FedEx", "UPS", "DHL"
    ]
    
    messages = []
    for i in range(num_messages):
        # Generate random time in the last 24 hours
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        msg_time = datetime.now() - timedelta(hours=hours_ago, minutes=minutes_ago)
        
        template = random.choice(message_templates)
        sender = random.choice(companies)
        code = random.randint(100000, 999999)
        amount = random.randint(10, 500)
        
        message_text = template.format(code=code, amount=amount)
        
        messages.append({
            'time': msg_time.strftime('%H:%M'),
            'date': msg_time.strftime('%Y-%m-%d'),
            'sender': sender,
            'message': message_text
        })
    
    # Sort by time (most recent first)
    messages.sort(key=lambda x: x['date'] + ' ' + x['time'], reverse=True)
    return messages

@app.route('/')
def index():
    """Homepage with country grid"""
    response = make_response(render_template('index.html', countries=COUNTRIES))
    # Cache for 1 hour since countries don't change
    response.headers['Cache-Control'] = 'public, max-age=3600, stale-while-revalidate=86400'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:"
    return response

@app.route('/country/<country_code>')
def country(country_code):
    """Country page with virtual phone numbers"""
    country_data = get_country_by_code(country_code)
    if not country_data:
        return redirect(url_for('index'))
    
    # Generate enhanced SEO data for the country
    country_data = generate_seo_data_for_country(country_data)
    phone_numbers = generate_phone_numbers(country_code)
    
    return render_template('country.html', 
                         country=country_data, 
                         phone_numbers=phone_numbers)

@app.route('/inbox/<country_code>/<phone_number>')
def inbox(country_code, phone_number):
    """Inbox page with SMS messages for a phone number"""
    country_data = get_country_by_code(country_code)
    if not country_data:
        return redirect(url_for('index'))
    
    # Add '+' back to phone number if missing
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    
    messages = generate_messages(country_code, phone_number)
    
    return render_template('inbox.html',
                         country=country_data,
                         phone_number=phone_number,
                         messages=messages)

@app.route('/sitemap')
def sitemap():
    """Simple sitemap page"""
    return render_template('sitemap.html', countries=COUNTRIES)

@app.route('/sitemap.xml')
def sitemap_xml():
    """XML sitemap for search engines"""
    from flask import Response
    
    # Generate XML sitemap content
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{}</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>'''.format(url_for('index', _external=True))
    
    # Add country pages
    for country in COUNTRIES:
        country_data = generate_seo_data_for_country(country)
        xml_content += '''
    <url>
        <loc>{}</loc>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>'''.format(url_for('country', country_code=country['code'], _external=True))
    
    # Add static pages
    static_pages = ['about', 'help', 'privacy', 'terms', 'sitemap']
    for page in static_pages:
        xml_content += '''
    <url>
        <loc>{}</loc>
        <changefreq>weekly</changefreq>
        <priority>0.5</priority>
    </url>'''.format(url_for(page, _external=True))
    
    xml_content += '''
</urlset>'''
    
    response = Response(xml_content, mimetype='application/xml')
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 24 hours
    return response

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/help')
def help():
    """Help and FAQ page"""
    return render_template('help.html')

@app.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    """Terms of service page"""
    return render_template('terms.html')



@app.route('/robots.txt')
def robots_txt():
    """Robots.txt file"""
    robots_content = f"""User-agent: *
Allow: /
Sitemap: {request.url_root}sitemap.xml

# Crawl-delay for better server performance
Crawl-delay: 1
"""
    response = make_response(robots_content)
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Cache-Control'] = 'public, max-age=86400'
    return response

@app.template_filter('regex_search')
def regex_search(s, pattern):
    """Template filter to search for regex patterns"""
    return bool(re.search(pattern, s))

@app.context_processor
def inject_current_year():
    """Inject current year into templates"""
    return {'current_year': datetime.now().year}