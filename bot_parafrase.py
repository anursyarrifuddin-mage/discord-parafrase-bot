import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

ACTIVE_MODEL = None 

class BotClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        print("🔄 Sinkronisasi Slash Commands...")
        await self.tree.sync()
        print("✅ Slash Commands Siap!")

bot = BotClient()

async def cari_model_otomatis():
    global ACTIVE_MODEL
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    
    print("🔄 Mencari model Google...")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                for m in data.get('models', []):
                    if 'generateContent' in m.get('supportedGenerationMethods', []):
                        ACTIVE_MODEL = m['name'] 
                        print(f"✅ Bot menggunakan: {ACTIVE_MODEL}")
                        return
                print("❌ Tidak ada model tersedia.")
            else:
                print(f"❌ Koneksi Gagal: {response.status}")

@bot.event
async def on_ready():
    print(f'🤖 Login sebagai {bot.user}')
    await cari_model_otomatis()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))

@bot.tree.command(name="help", description="Tampilkan panduan penggunaan bot")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📘 Dokumentasi Bot Parafrase",
        description=(
            "Bot ini menggunakan teknologi **Generative AI** untuk menulis ulang (parafrase) teks "
            "dengan mempertahankan makna asli namun mengubah struktur kalimat agar terlihat "
            "natural dan lolos deteksi AI."
        ),
        color=0x3498db
    )

    embed.add_field(
        name="🚀 Cara Penggunaan",
        value="Gunakan perintah slash berikut:\n```/parafrase [gaya] [teks]```",
        inline=False
    )

    embed.add_field(
        name="🎨 Opsi Gaya Bahasa",
        value=(
            "• **Formal**: Bahasa baku, akademis, cocok untuk skripsi/jurnal.\n"
            "• **Santai**: Bahasa percakapan sehari-hari (kasual).\n"
            "• **Jaksel**: Campuran Bahasa Indonesia & Inggris (Code-mixing).\n"
            "• **Lucu**: Nada humoris, jenaka, dan santai.\n"
            "• **Inggris**: Penerjemahan ke Bahasa Inggris dengan grammar natural."
        ),
        inline=False
    )

    embed.set_footer(
        text="Developed with ☕ by Aldi | Powered by Gemini AI",
        icon_url=interaction.user.display_avatar.url
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="parafrase", description="Ubah kalimat jadi lebih manusiawi")
@app_commands.describe(teks="Masukkan teks yang mau diubah")
@app_commands.choices(gaya=[
    app_commands.Choice(name="Formal", value="formal"),
    app_commands.Choice(name="Santai", value="santai"),
    app_commands.Choice(name="Jaksel", value="jaksel"),
    app_commands.Choice(name="Lucu", value="lucu"),
    app_commands.Choice(name="English", value="inggris")
])
async def parafrase_slash(interaction: discord.Interaction, gaya: app_commands.Choice[str], teks: str):
    await interaction.response.defer()

    if not ACTIVE_MODEL:
        await interaction.followup.send("⚠️ Sedang mencari koneksi server... Coba lagi nanti.")
        await cari_model_otomatis()
        return

    selected_style = gaya.value
    
    if selected_style == 'formal':
        instr = "bahasa baku, akademis, profesional"
        label = "Formal 🧐"
    elif selected_style == 'santai':
        instr = "bahasa gaul, santai"
        label = "Santai 😎"
    elif selected_style == 'jaksel':
        instr = "gaya anak Jakarta Selatan (campur Inggris/Indo)"
        label = "Anak Jaksel ☕"
    elif selected_style == 'lucu':
        instr = "humoris, jenaka"
        label = "Lucu 🤣"
    elif selected_style == 'inggris':
        instr = "Bahasa Inggris natural"
        label = "English 🇬🇧"
    else:
        instr = "bahasa Indonesia natural"
        label = "Netral"

    prompt = (
        f"Bertindaklah sebagai Dosen Pembimbing atau Editor Jurnal Akademik profesional. "
        f"Tugasmu adalah menulis ulang (rephrase) teks berikut agar cocok untuk Skripsi/Makalah Ilmiah.\n"
        f"Target Gaya: {instr}.\n\n"
        f"INSTRUKSI PENULISAN (WAJIB):\n"
        f"1. STRUKTUR KALIMAT MAJEMUK: Hindari kalimat yang terlalu pendek atau terpotong-potong. Gunakan kalimat majemuk bertingkat yang mengalir (flow) dengan kata penghubung yang tepat (koherensi).\n"
        f"2. KOSAKATA AKADEMIS VARIATIF: Jangan gunakan kata 'standar' AI berulang-ulang. Gunakan sinonim akademis yang lebih luwes. (Contoh: alih-alih 'hal ini menunjukkan', gunakan 'fenomena ini mengindikasikan').\n"
        f"3. HINDARI POLA ROBOT: Jangan selalu memulai kalimat dengan Subjek. Sesekali awali dengan Keterangan Waktu, Anak Kalimat, atau Frasa Preposisi untuk memecah pola monoton.\n"
        f"4. PERTAHANKAN MAKNA ILMIAH: Jangan ubah istilah teknis penting, tapi ubah cara penjelasannya agar terdengar seperti analisis mendalam manusia, bukan ringkasan mesin.\n"
        f"5. TUJUAN: Hasilkan teks yang 100% formal, baku (PUEBI), namun memiliki 'ritme' penulisan manusia yang natural.\n\n"
        f"Teks asli: {teks}"
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/{ACTIVE_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.85,     # Turunkan dikit biar gak ngelantur kayak puisi
            "topP": 0.95,            # Tetap tinggi biar kosakata luas
            "topK": 40
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    try:
                        hasil = data['candidates'][0]['content']['parts'][0]['text']
                        if len(hasil) <= 4000:
                            embed = discord.Embed(title=f"✨ Hasil Parafrase ({label})", color=0x2ecc71)
                            embed.description = hasil 
                            embed.set_footer(text=f"Request by {interaction.user.name}")
                            
                            await interaction.followup.send(embed=embed)
                        else:
                            import io
                            buffer = io.BytesIO(hasil.encode('utf-8'))
                            file_discord = discord.File(buffer, filename=f"hasil_{selected_style}.txt")
                            
                            await interaction.followup.send(
                                content=f"✅ **Selesai!** Karena hasilnya panjang ({len(hasil)} karakter), saya kirim via file:",
                                file=file_discord
                            )

                    except Exception as e:
                        await interaction.followup.send(f"⚠️ Gagal memproses data: {e}")
                else:
                    await interaction.followup.send(f"⚠️ Error Google (Status {response.status})")
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error Koneksi: {e}")

bot.run(DISCORD_TOKEN)