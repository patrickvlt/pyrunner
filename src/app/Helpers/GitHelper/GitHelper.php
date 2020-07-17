<?php

if (!function_exists('gitlab')) {
    function gitlab($url,$method='GET',$post_data=null)
    {
        $token = isset(auth()->user()->gitlab_token) && !empty(auth()->user()->gitlab_token) ? decrypt(auth()->user()->gitlab_token) : '';
        if (empty($token)){
            $token = (env('GITLAB_TOKEN') !== null) && !empty(env('GITLAB_TOKEN')) ? decrypt(env('GITLAB_TOKEN')) : '';
        }
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            "Private-Token: ".$token.""
            ]);  
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
        $result = curl_exec($ch);
        return json_decode($result);
    }
}

if (!function_exists('github')) {
    function github($url,$method='GET',$post_data=null)
    {
        $token = isset(auth()->user()->github_token) && !empty(auth()->user()->github_token) ? decrypt(auth()->user()->github_token) : '';
        if (empty($token)){
            $token = (env('GITHUB_TOKEN') !== null) && !empty(env('GITHUB_TOKEN')) ? decrypt(env('GITHUB_TOKEN')) : '';
        }
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            "Authorization: token ".$token."",
            "Accept: application/vnd.github.v3.full+json",
            "User-Agent: Awesome-Octocat-App"
            ]);  
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
        $result = curl_exec($ch);
        return json_decode($result);
    }
}