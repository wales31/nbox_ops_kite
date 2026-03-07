package co.ixafrica.opspulse.network

import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory

object ApiProvider {
    private val moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()

    fun create(baseUrl: String): OpsPulseApi {
        return Retrofit.Builder()
            .baseUrl(baseUrl.ensureTrailingSlash())
            .addConverterFactory(MoshiConverterFactory.create(moshi))
            .build()
            .create(OpsPulseApi::class.java)
    }
}

private fun String.ensureTrailingSlash(): String = if (endsWith("/")) this else "$this/"

