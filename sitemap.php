<?php
require_once 'countries.php';

header('Content-Type: text/xml; charset=utf-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <!-- Homepage -->
    <url>
        <loc><?= htmlspecialchars('http://' . $_SERVER['HTTP_HOST']) ?>/</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
        <lastmod><?= date('Y-m-d') ?></lastmod>
    </url>
    
    <!-- Countries -->
    <?php foreach ($countries as $country): ?>
    <url>
        <loc><?= htmlspecialchars('http://' . $_SERVER['HTTP_HOST'] . '/country.php?cc=' . urlencode($country['cc'])) ?></loc>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
        <lastmod><?= date('Y-m-d') ?></lastmod>
    </url>
    <?php endforeach; ?>
    
    <!-- Sitemap -->
    <url>
        <loc><?= htmlspecialchars('http://' . $_SERVER['HTTP_HOST'] . '/sitemap.php') ?></loc>
        <changefreq>weekly</changefreq>
        <priority>0.3</priority>
        <lastmod><?= date('Y-m-d') ?></lastmod>
    </url>
</urlset>
