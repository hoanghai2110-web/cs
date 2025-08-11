<?php
require_once 'countries.php';
require_once 'partials/header.php';

// Get parameters from URL
$cc = isset($_GET['cc']) ? strtoupper($_GET['cc']) : '';
$number = isset($_GET['n']) ? $_GET['n'] : '';

// Find country data
$currentCountry = null;
foreach ($countries as $country) {
    if ($country['cc'] === $cc) {
        $currentCountry = $country;
        break;
    }
}

// Redirect if country not found or number missing
if (!$currentCountry || !$number) {
    header('Location: index.php');
    exit;
}

// Generate fake SMS messages
function fakeMessages($cc, $number) {
    // Seed with country, number, and current date for consistent daily messages
    mt_srand(crc32($cc . $number . date('Y-m-d')));
    
    $messagePool = [
        "Your login code is %d. Expires in 5 minutes.",
        "Your verification code is %d. Do not share this code.",
        "Monzo: Confirm payment £%.2f, code %d",
        "Your Amazon verification code is %d",
        "Netflix: Your verification code is %d",
        "PayPal: Your security code is %d",
        "WhatsApp code: %d. Don't share this code.",
        "Royal Mail: Your parcel tracking code is %d",
        "Uber: Your verification code is %d",
        "Facebook: Your confirmation code is %d",
        "Google: %d is your verification code",
        "Instagram: Use %d to verify your account",
        "Twitter: Your verification code is %d",
        "LinkedIn: Your verification code is %d",
        "Spotify: Your verification code is %d",
        "Apple ID: Your verification code is %d",
        "Microsoft: Your security code is %d",
        "Binance: Your verification code is %d",
        "Coinbase: Your verification code is %d",
        "Steam: Your verification code is %d",
        "Discord: Your verification code is %d",
        "Telegram: Your login code is %d",
        "Signal: Your verification code is %d",
        "DHL: Package update. Tracking code: %d",
        "FedEx: Delivery scheduled. Code: %d",
        "UPS: Package status update. Code: %d",
        "HSBC: Transaction alert. Code: %d",
        "Barclays: Security verification. Code: %d",
        "Santander: Login verification. Code: %d",
        "Lloyds: Payment confirmation. Code: %d"
    ];
    
    $senders = [
        "Amazon", "Google", "PayPal", "Netflix", "Facebook", "Apple", "Microsoft",
        "WhatsApp", "Instagram", "Twitter", "LinkedIn", "Uber", "Spotify",
        "Royal Mail", "DHL", "FedEx", "UPS", "Monzo", "HSBC", "Barclays",
        "Santander", "Lloyds", "Binance", "Coinbase", "Steam", "Discord",
        "Telegram", "Signal", "Verification", "Security"
    ];
    
    $messages = [];
    $messageCount = mt_rand(8, 15);
    
    for ($i = 0; $i < $messageCount; $i++) {
        $template = $messagePool[mt_rand(0, count($messagePool) - 1)];
        $sender = $senders[mt_rand(0, count($senders) - 1)];
        $code = mt_rand(100000, 999999);
        $amount = mt_rand(500, 15000) / 100; // Random amount for payment messages
        
        // Format message with appropriate values
        if (strpos($template, '£%.2f') !== false) {
            $messageText = sprintf($template, $amount, $code);
        } else {
            $messageText = sprintf($template, $code);
        }
        
        // Generate timestamp (within last 2 hours)
        $minutesAgo = mt_rand(5, 120);
        $timestamp = time() - ($minutesAgo * 60);
        
        $messages[] = [
            'from' => $sender,
            'message' => $messageText,
            'time' => $timestamp,
            'code' => $code
        ];
    }
    
    // Sort by time (newest first)
    usort($messages, function($a, $b) {
        return $b['time'] - $a['time'];
    });
    
    return $messages;
}

$messages = fakeMessages($cc, $number);

// Extract codes for easy copying
function extractCode($message) {
    if (preg_match('/\b(\d{4,8})\b/', $message, $matches)) {
        return $matches[1];
    }
    return null;
}
?>

<!-- Auto refresh every 30 seconds -->
<meta http-equiv="refresh" content="30">

<div class="min-h-screen bg-gray-50">
    <!-- Breadcrumb -->
    <div class="bg-white border-b">
        <div class="container mx-auto px-4 py-3">
            <nav class="text-sm">
                <a href="index.php" class="text-blue-600 hover:text-blue-800">All countries</a>
                <span class="mx-2 text-gray-400">→</span>
                <a href="country.php?cc=<?= urlencode($cc) ?>" class="text-blue-600 hover:text-blue-800"><?= htmlspecialchars($currentCountry['name']) ?></a>
                <span class="mx-2 text-gray-400">→</span>
                <span class="text-gray-600">+<?= htmlspecialchars($number) ?></span>
            </nav>
        </div>
    </div>

    <div class="container mx-auto px-4 py-6">
        <!-- Phone Number Header -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="flex items-center justify-between">
                <div class="flex items-center">
                    <div class="text-3xl mr-4"><?= $currentCountry['flag'] ?></div>
                    <div>
                        <h1 class="text-2xl font-bold text-gray-900">+<?= htmlspecialchars($number) ?></h1>
                        <p class="text-gray-600"><?= htmlspecialchars($currentCountry['name']) ?> • Virtual Number</p>
                    </div>
                </div>
                <div class="text-right">
                    <div class="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">
                        Auto-refresh: 30s
                    </div>
                </div>
            </div>
        </div>

        <!-- Demo Warning -->
        <div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div class="flex">
                <svg class="h-5 w-5 text-red-400 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                </svg>
                <div>
                    <h3 class="text-sm font-medium text-red-800">Sandbox Demo</h3>
                    <p class="text-sm text-red-700 mt-1">All messages are generated and not real. This is for demonstration purposes only.</p>
                </div>
            </div>
        </div>

        <!-- Messages Table -->
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="px-6 py-4 bg-gray-50 border-b">
                <h2 class="text-lg font-semibold text-gray-900">Received Messages (<?= count($messages) ?>)</h2>
            </div>
            
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">From</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Message</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Code</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <?php foreach ($messages as $msg): ?>
                            <tr class="hover:bg-gray-50">
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm font-medium text-gray-900"><?= htmlspecialchars($msg['from']) ?></div>
                                </td>
                                <td class="px-6 py-4">
                                    <div class="text-sm text-gray-900 max-w-xs lg:max-w-md xl:max-w-lg">
                                        <?= htmlspecialchars($msg['message']) ?>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <?php $code = extractCode($msg['message']); ?>
                                    <?php if ($code): ?>
                                        <input type="text" value="<?= htmlspecialchars($code) ?>" readonly 
                                               class="text-sm font-mono bg-gray-100 border-0 px-2 py-1 rounded w-20 text-center cursor-pointer select-all"
                                               onclick="this.select()">
                                    <?php else: ?>
                                        <span class="text-gray-400 text-sm">-</span>
                                    <?php endif; ?>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    <?= date('H:i', $msg['time']) ?>
                                    <div class="text-xs text-gray-400"><?= date('M j', $msg['time']) ?></div>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Instructions -->
        <div class="mt-6 bg-blue-50 rounded-lg p-6">
            <h3 class="text-lg font-semibold text-blue-900 mb-3">How to copy codes</h3>
            <div class="text-blue-700 text-sm space-y-2">
                <p>• Click on any code in the "Code" column to select it automatically</p>
                <p>• Use Ctrl+C (Windows/Linux) or Cmd+C (Mac) to copy the selected code</p>
                <p>• Page refreshes every 30 seconds to simulate new messages</p>
                <p>• All codes and messages are generated for demonstration purposes only</p>
            </div>
        </div>
    </div>
</div>

<?php require_once 'partials/footer.php'; ?>
