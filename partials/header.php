<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <?php
    // Dynamic SEO based on current page
    $current_page = basename($_SERVER['PHP_SELF'], '.php');
    $page_title = "SMS Receiver Sandbox";
    $page_description = "Demo SMS receiver with virtual phone numbers from 100+ countries. Test SMS reception without real phone numbers.";
    
    if ($current_page === 'country' && isset($currentCountry)) {
        $page_title = "Virtual Numbers for " . $currentCountry['name'] . " - SMS Receiver";
        $page_description = "Virtual phone numbers for " . $currentCountry['name'] . ". Receive demo SMS messages for testing purposes.";
    } elseif ($current_page === 'inbox' && isset($currentCountry, $number)) {
        $page_title = "SMS Inbox +" . $number . " (" . $currentCountry['name'] . ") - SMS Receiver";
        $page_description = "View demo SMS messages received on virtual number +" . $number . " from " . $currentCountry['name'] . ".";
    }
    ?>
    
    <title><?= htmlspecialchars($page_title) ?></title>
    <meta name="description" content="<?= htmlspecialchars($page_description) ?>">
    <meta name="keywords" content="SMS receiver, virtual phone numbers, demo SMS, fake SMS, receive SMS online, temporary phone numbers">
    <meta name="robots" content="index, follow">
    
    <!-- Open Graph -->
    <meta property="og:title" content="<?= htmlspecialchars($page_title) ?>">
    <meta property="og:description" content="<?= htmlspecialchars($page_description) ?>">
    <meta property="og:type" content="website">
    <meta property="og:url" content="<?= htmlspecialchars($_SERVER['REQUEST_URI']) ?>">
    
    <!-- TailwindCSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Custom styles -->
    <style>
        .select-all:focus {
            background-color: #dbeafe;
        }
    </style>
</head>
<body class="bg-gray-50">
